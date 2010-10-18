# 10/13/10
# Charles O. Goddard

import socket
import struct
import threading
import select
import cPickle
import os
import time
import tempfile
import random

import psycopg2
import data
import db

# This ranks pretty high on my list of favorite variable names.
# TODO: Make this less appalling.
hardcoded_connection_string_in_plaintext = "dbname=test user=postgres password=TzjUvh"

class Downloader(threading.Thread):
    '''Thread subclass for asynchronous file downloading and insertion
    into database'''
    def __init__(self, fd, source, path, dest):
        # Normally I'd be more cautious about sharing a variable across
        # threads. However, as only one will be writing and only one will be
        # reading (in conjunction with the GIL,) the worst case scenario here
        # is that a fetched progress value will be slightly out of date.
        self.progress = 0.0
        
        # This looks totally superfluous, but it's actually opening a new
        # connection to the data source. Sockets are one of many things
        # I find not at all fun to share across threads.
        self._source = cPickle.loads(cPickle.dumps(source,protocol=2))
        self._path = path
        self._dest = dest
        self._fd = fd
        super(Downloader, self).__init__()
    
    def _callback(self, prog):
        self.progress = prog
    
    def _download(self, out, i=0):
        if i > 4:
            self.progress = 0.0
            return
        try:
            self._source.download(self._path, out.name, self._callback)
        except socket.error:
            time.sleep(5)
            self._source = cPickle.loads(cPickle.dumps(self._source))
            self._download(out, i+1)
        self.progress = 1.0
    
    def run(self):
        out = tempfile.NamedTemporaryFile('w')
        self._download(out)
        
        fs = db.FileStore(hardcoded_connection_string_in_plaintext)
        try:
            f = fs.new(self._dest, out.name)
            f.owner = 'root'
            f.original_path = os.path.join(self._source.name(), self._path)
        except:
            fs.rollback()
        else:
            fs.commit()
        out.close()
        

class FetchD(object):
    '''Daemon providing persistent connections to data sources'''
    def __init__(self):
        self.sources = {}
        self.downloads = {}
        self.last_query = time.time()
        self.sock = None
    
    def check_source(self, src):
        '''Returns a string describing any problems with a source, or None
        if okay.'''
        if src in self.sources:
            try:
                self.sources[src].listdir('/')
            except:
                pass
            else:
                return None
        (type, usn, pwd) = cPickle.loads(src)
        try:
            source = data.sources[type](usn, pwd)
        except data.LoginError:
            return 'Failed to log in'
        except socket.error:
            return 'Failed to connect'
        else:
            self.sources[src] = source
        return None
    
    def wrap_dir(self, source, dir):
        return [(name, source.isdir(os.path.join(dir,name))) for
                name in source.listdir(dir)]
    
    #
    #  Exposed services
    #
    
    def f_progress(self, client, (download,)):
        download = int(download)
        if not download in self.downloads:
            client.send("error\x00%s\x00No such download\x01"%(download))
            return
        progress = self.downloads[download].progress
        client.send("progress\x00%s\x00%f\x01"%(download, progress))
    
    def f_dir(self, client, (src, dir)):
        err = self.check_source(src)
        if err:
            client.send("error\x00%s\x01"%(err))
        source = self.sources[src]
        msg = "dir\x00%s\x00%s\x00%s\x01" % (src,
                                dir,
                                cPickle.dumps(self.wrap_dir(source, dir),
                                              protocol=0))
        client.send(msg)
    
    def f_download(self, client, (src, path, dest)):
        err = self.check_source(src)
        if err:
            client.send("error\x00%s\x01"%(err))
            return
        fs = db.FileStore(hardcoded_connection_string_in_plaintext)
        if fs.name_exists(dest) or dest in [d._dest for d in self.downloads.values()]:
            client.send("error\x00Name already exists\x01")
            return
        source = self.sources[src]
        if not source.isfile(path):
            client.send("error\x00Not a file\x01")
            return
        
        new_idx = random.randint(0, 0xFFFFFFFF)
        while new_idx in self.downloads:
            new_idx = random.randint(0, 0xFFFFFFFF)
            time.sleep(0.0)
        self.downloads[new_idx] = Downloader(self, source, path, dest)
        self.downloads[new_idx].start()
        client.send("download\x00%s\x01"%(new_idx,))
    
    #
    # Main function
    #
    
    def run(self, addr="/tmp/cg_fetchd"):
        # Socket setup
        try:
            os.unlink(addr)
        except OSError:
            pass
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.bind(addr)
        self.sock.listen(5)
        
        # Listen loop
        clients = []
        cdata = {}
        print 'listening'
        while True:
            frame_begin = time.time()
            # Check if a new connection is pending
            (newconn, _, _) = select.select([self.sock], [], [], 0.8)
            if newconn:
                (conn, _) = self.sock.accept()
                clients.append(conn)
                cdata[conn] = [[], frame_begin]
            
            # Read and handle all incoming requests
            (ready, _, _) = select.select(clients, [], [], 0.2)
            if not ready:
                continue
            for client in ready:
                buf = cdata[client][0]
                datagram = client.recv(1024)
                if not datagram:
                    clients.remove(client)
                    continue
                buf.append(datagram)
                cdata[client][1] = frame_begin
                self.last_query = frame_begin
                
                # Continue reading until end of message has been reached
                if buf[-1][-1] != '\x01':
                    continue
                
                # Handle completed message
                msg = (''.join(buf)[:-1]).split("\x00")
                cdata[client][0] = []
                func = "f_"+msg[0]
                if hasattr(self, func):
                    try:
                        getattr(self, func)(client, msg[1:])
                    except Exception, e:
                        raise
                        #print e
            # Drop any connections that have been open for more than 5
            # minutes without activity
            dead = [c for c in clients if
                    frame_begin - cdata[c][1] > 60*5]
            for d in dead:
                d.close()
                clients.remove(d)
                del cdata[d]
            # Check time inactive & quit if appropriate
            if time.time() - self.last_query > 60 * 30:
                break
        print 'stopping due to inactivity'
        for d in self.downloads:
            d.join()

if __name__ == '__main__':
    f = FetchD()
    try:
        f.run()
    finally:
        os.unlink('/tmp/cg_fetchd')