# 10/10/10
# Charles O. Goddard
'''
Light abstraction layer for data sources
'''

import ftputil
import orbiter
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
    
    def listdir(self, path=''):
        raise NotImplementedError()
    
    def isdir(self, path):
        raise NotImplementedError()
    
    def isfile(self, path):
        raise NotImplementedError()
    
    def download(self, path, dest):
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
    
    def download(self, path, dest):
        return self.ftp.download(path, dest, 'b')
    
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
        cur = filter(lambda ap:ap.path==volume)[0]
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
    
    def download(self, path, dest):
        node = self.path_to_node(path)
        url = self.orb.fileurl(node)
        return urllib.urlretrieve(url, dest)
    
    def name(self):
        return 'ORNL'

sources = {'NIST': lambda usn,pwd: FTPSource('ftp.ncnr.nist.gov',usn,pwd),
           'ORNL': OrbiterSource}