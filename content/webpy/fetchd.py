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
        
        self._source = source
        self._path = path
        self._dest = dest
        self._fd = fd
        super(Downloader, self).__init__()
    
    def _callback(self, prog):
        self.progress = prog
    
    def run(self):
        out = tempfile.NamedTemporaryFile('w')
        self._source.download(self._path, out.name, self._callback)
        self.progress = 1.0
        
        fs = db.FileStore(hardcoded_connection_string_in_plaintext)
        f = fs.new(self._dest, out.name)
        f.owner = 'root'
        f.original_path = os.path.join(self._source.name(), self._path)
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
                self.sources[src].isdir('/')
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
            client.send("error\x00%s\x00No such download"%(download))
            return
        progress = self.downloads[download].progress
        client.send("progress\x00%s\x00%f"%(download, progress))
    
    def f_dir(self, client, (src, dir)):
        err = self.check_source(src)
        if err:
            client.send("error\x00%s"%(err))
        source = self.sources[src]
        msg = "dir\x00%s\x00%s\x00%s" % (src,
                                dir,
                                cPickle.dumps(self.wrap_dir(source, dir),
                                              protocol=0))
        client.send(msg)
    
    def f_download(self, client, (src, path, dest)):
        err = self.check_source(src)
        if err:
            client.send("error\x00%s"%(err))
            return
        fs = db.FileStore(hardcoded_connection_string_in_plaintext)
        if fs.name_exists(dest):
            client.send("error\x00Name already exists")
            return
        source = self.sources[src]
        if not source.isfile(path):
            client.send("error\x00Not a file")
            return
        
        new_idx = random.randint(0, 0xFFFFFFFF)
        while new_idx in self.downloads:
            new_idx = random.randint(0, 0xFFFFFFFF)
        self.downloads[new_idx] = Downloader(self, source, path, dest)
        self.downloads[new_idx].start()
        client.send("download\x00%s"%(new_idx,))
    
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
        self.sock.listen(4)
        
        # Listen loop
        clients = []
        print 'listening'
        while True:
            (newconn, _, _) = select.select([self.sock], [], [], 0.0)
            if newconn:
                (conn, _) = self.sock.accept()
                clients.append(conn)
            
            (ready, _, _) = select.select(clients, [], [], 0.0)
            if not ready:
                continue
            for client in ready:
                datagram = client.recv(1024)
                if not datagram:
                    clients.remove(client)
                    continue
                self.last_query = time.time()
                msg = datagram.split("\x00")
                func = "f_"+msg[0]
                if hasattr(self, func):
                    try:
                        getattr(self, func)(client, msg[1:])
                    except Exception, e:
                        raise
                        #print e
            if time.time() - self.last_query > 60 * 30:
                break
            time.sleep(0.0)
        print 'stopping due to inactivity'
        for d in self.downloads:
            d.join()
        try:
            os.unlink(addr)
        except OSError:
            pass

if __name__ == '__main__':
    f = FetchD()
    try:
        f.run()
    except:
        pass
    os.unlink('/tmp/cg_fetchd')