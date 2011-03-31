# 10/10/10
# Charles O. Goddard
'''
Light abstraction layer for data sources
'''

import ftputil
import os
#import orbiter
import urllib

class LoginError(IOError):
    pass

class DataSource(object):
    def __init__(self, *args):
        self._args = args
    
    def __getstate__(self):
        return self._args
    def __setstate__(self, state):
        self.__init__(*state)
    
    def clone(self):
        return type(self)(*self._args)
    
    def listdir(self, path=''):
        raise NotImplementedError()
    
    def isdir(self, path):
        raise NotImplementedError()
    
    def isfile(self, path):
        raise NotImplementedError()
    
    def download(self, path, dest, callback):
        '''
        callback should accept one parameter - progress, as a number
        between zero and one
        '''
        raise NotImplementedError()
    
    def name(self):
        raise NotImplementedError()

#
# FTP data source
#

class FTPSource(DataSource):
    def __init__(self, host, username='', pwd=''):
        try:
            self.ftp = ftputil.FTPHost(host, username or 'anonymous', pwd)
        except ftputil.ftp_error.FTPError, e:
            raise LoginError(e)
        super(FTPSource, self).__init__(host, username, pwd)
    
    def listdir(self, path=''):
        return self.ftp.listdir(path)
    
    def isdir(self, path):
        return self.ftp.path.isdir(path)
    
    def isfile(self, path):
        return self.ftp.path.isfile(path)
    
    def download(self, path, dest, callback):
        sz = float(self.ftp.stat(path)[6]) # st_size
        def cb(c, p=[0]):
            p[0] += len(c)
            callback(p[0] / sz)
        return self.ftp.download(path, dest, 'b', cb)
    def name(self):
        return self._args[0]

#
# ORNL Orbiter data source
#

class OrbiterSource(DataSource):
    def __init__(self, username, pwd):
        print username, pwd
        urllib._urlopener = urllib.FancyURLopener()
        urllib._urlopener.prompt_user_passwd = lambda self,h,r: (username, pwd)
        self.orb = orbiter.connect()
    
    def path_to_node(self, path):
        '''Translate a path passed to the script to a node.'''
        chunks = path.split('/')
        volume = chunks.pop(0)
        cur = filter(lambda ap:ap.path==volume, self.orb.volumes())[0]
        while chunks:
            next = chunks.pop(0)
            dirs = self.orb.directories(cur)
            dirs = filter(lambda d: d.name == next, dirs)
            if dirs:
                cur = dirs[0]
            elif not chunks:
                files = self.orb.files(cur)
                files = filter(lambda f: f.name == next, files)
                if files:
                    cur = files[0]
            else:
                raise IOError("file not found")
        return cur
    
    def listdir(self, path):
        if not path:
            return map(lambda ap: ap.path, self.orb.volumes())
        node = self.path_to_node(path)
        dir = self.orb.directories(node) + self.orb.files(node)
        return map(lambda e: e.name, dir)
    
    def isdir(self, path):
        node = self.path_to_node(path)
        return hasattr(node, 'volume')

    def isfile(self, path):
        return not self.isdir(path)
    
    def download(self, path, dest, callback):
        node = self.path_to_node(path)
        url = self.orb.fileurl(node)
        def cb(blocks, bs, total):
            callback(blocks*bs / float(total))
        return urllib.urlretrieve(url, dest, cb)
    
    def name(self):
        return 'ORNL'

class LocalSource(DataSource):
    def __init__(self, base, usn, pwd):
        self.base = base
        super(LocalSource, self).__init__(base, usn, pwd)
    def listdir(self, path=''):
        return os.listdir(self.base+path)
    
    def isdir(self, path):
        return os.path.isdir(self.base+path)
    
    def isfile(self, path):
        return os.path.isfile(self.base+path)
    
    def download(self, path, dest, callback):
        open(dest,'wb').write(open(self.base+path,'rb').read())
        callback(1.0)
    
    def name(self):
        return "localhost"

sources = {'NIST': lambda usn,pwd: FTPSource('ftp.ncnr.nist.gov',usn,pwd),
           'ORNL': OrbiterSource}#,
#           'DANSE Folder':lambda usn,pwd: LocalSource('/Volumes/DANSE/',usn,pwd),
#           'Root Folder':lambda usn,pwd: LocalSource('/',usn,pwd)}
