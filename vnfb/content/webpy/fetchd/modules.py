# 10/18/10
# Charles O. Goddard

import threading
import tempfile
import cPickle
import random
import time
import zlib
import os

import data
import db
from public import *

class Module(object):
    def __init__(self, core):
        for name in self.exposed:
            core.services[name] = getattr(self, name)
    
    def maintain(self):
        '''
        Should perform any maintenance necessary on a module - cleanup
        of unused resources, etc. Called approx. every 10 seconds.
        '''
        pass

#
# Download functionality
#

class ActiveDownload(threading.Thread):
    def __init__(self, source, path, dest):
        # These three variables are written to exclusively by the 
        # downloading thread and read exclusively by the main thread.
        # This is why I'm performing no synchronization on them.
        self.progress = 0.0
        self.status = DS_STARTING
        self.error = ""
        
        self.last_access = time.time()
        
        self._source = source.clone()
        self._path = path
        self._dest = dest
        super(ActiveDownload, self).__init__()
    
    @property
    def source(self):
        return self._source
    @property
    def path(self):
        return self._path
    @property
    def dest(self):
        return self._dest
    
    def __update_progress(self, val):
        self.progress = val
    
    def run(self):
        path, dest, source = self._path, self._dest, self._source
        try:
            out = tempfile.NamedTemporaryFile('w')
            source.download(path, out.name, self.__update_progress)
        except Exception, e:
            self.error = str(e)
            self.status = DS_FAILED
            return
        self.progress = 1.0
        self.status = DS_LOADING
        
        try:
            fs = db.FileStore()
            f = fs.new(dest, out.name)
            f.original_path = os.path.join(source.name(), path)
            f.owner = 'root'
        except Exception, e:
            fs.conn.rollback()
            self.status = DS_FAILED
            self.error = str(e)
        else:
            fs.commit()
            self.status = DS_DONE
        return 0

class DownloadModule(Module):
    exposed = ['status', 'download']
    def __init__(self, core):
        self.downloads = {}
        super(DownloadModule, self).__init__(core)
    
    def status(self, client, (download_id,)):
        if not download_id in self.downloads:
            client.send(Message(['error','No such download.']))
            return
        dl = self.downloads[download_id]
        dl.last_access = time.time()
        client.send(Message([download_id,
                             dl.status,
                             int(dl.progress * 100),
                             dl.error]))
    
    def download(self, client, (src, path, dest)):
        fs = db.FileStore()
        if fs.name_exists(dest) or dest in [d.dest for d in self.downloads.values()]:
            client.send(Message(['error', 'Name already exists in database']))
            return
        params = cPickle.loads(src)
        source = data.sources[params[0]](*params[1:])

        new_id = random.randint(0, 0xFFFFFFFF)#zlib.adler32(source.name() + path + dest) & 0xffffffff
        try:
            self.downloads[new_id] = ActiveDownload(source, path, dest)
        except data.LoginError, e:
            client.send(Message(['error', str(e)]))
            return
        self.downloads[new_id].start()
        msg = Message(['download',new_id])
        client.send(msg)
    
    def maintain(self):
        for k in self.downloads.keys():
            d = self.downloads[k]
            if d.last_access + 60*5 > time.time():
                continue
            if d.status in (DS_DONE, DS_FAILED):
                del self.downloads[k]
#
# Path functionality
#

class PathModule(Module):
    exposed = ['dir', 'isdir', 'isfile']
    def __init__(self, core):
        self.sources = {}
        super(PathModule, self).__init__(core)
    
    def get_source(self, src):
        if src in self.sources:
            try:
                self.sources[src].listdir('/')
            except:
                pass
            else:
                self.sources[src].last_use = time.time()
                return self.sources[src]
        params = cPickle.loads(src)
        self.sources[src] = data.sources[params[0]](*params[1:])
        self.sources[src].last_use = time.time()
        return self.sources[src]
    
    def _wrap(self, source, dir):
        try:
            return [(name, source.isdir(os.path.join(dir,name))) for
                    name in source.listdir(dir)]
        except Exception, e:
            return [(str(e), False)]
    
    def dir(self, client, (src, path)):
        print src, path
        source = self.get_source(src)
        client.send(Message(['dir', cPickle.dumps(self._wrap(source, path))]))
    
    def isdir(self, client, (src, path)):
        source = self.get_source(src)
        client.send(Message(['isdir',int(source.isdir(path))]))
    
    def isfile(self, client, (src, path)):
        source = self.get_source(src)
        client.send(Message(['isdir',int(source.isfile(path))]))
    
    def maintain(self):
        dead = [k for k in self.sources if
                self.sources[k].last_use + 60*5 <= time.time()]
        for d in dead:
            del self.sources[d]

#
# Module list
#

exposed = [DownloadModule, PathModule]