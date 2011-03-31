# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component as base

class DistributedDataStorage(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        dataroot = pyre.inventory.str('dataroot', default='../content/data')


    def add_server(self, server):
        node = _node(server)
        self._engine().add_node(node)
        return


    def remember(self, dbrecord, filename=None, server=None, files=list()):
        files = _files(dbrecord, filename=filename, files=files)
        for f in files:
            path = self.path(dbrecord, f)
            self._remember(path, server=server)
            continue
        return


    def forget(self, dbrecord, filename=None, server=None, files=list()):
        files = _files(dbrecord, filename=filename, files=files)
        for f in files:
            path = self.path(dbrecord, f)
            self._remove(path, server=server)
            self._forget(path, server=server)
            continue
        return


    def getmtime(self, dbrecord, filename=None, server=None):
        path = self.abspath(dbrecord, filename=filename, server=server)
        cmd = '. ~/.vnf; getmtime.py --path="%s"' % path
        failed, output, error = self.director.csaccessor.execute(cmd, server, '/tmp')

        # no output means the directory does not exist in the server
        if not output: return

        mtime = eval(output)
        return mtime        


    def move(self, dbrecord1, filename1, dbrecord2, filename2, server=None):
        path1 = self.path(dbrecord1, filename1)
        path2 = self.path(dbrecord2, filename2)
        return self._rename(path1, path2, server=server)


    def copy(self, dbrecord1, filename1, dbrecord2, filename2, server=None):
        path1 = self.path(dbrecord1, filename1)
        path2 = self.path(dbrecord2, filename2)
        return self._copy(path1, path2, server=server)


    # do we assume this is a sym link from filename1 to filename2?
    def symlink(self, dbrecord1, filename1, dbrecord2, filename2, server=None):
        path1 = self.path(dbrecord1, filename1)
        path2 = self.path(dbrecord2, filename2)
        return self._symlink(path1, path2, server=server)


    def make_available(self, dbrecord, files=None, server=None, ignore_nonexisting_files=False):
        if files is None: files = _default_files(dbrecord)
        for f in files:
            if not self.existssomewhere(dbrecord, f):
                if ignore_nonexisting_files:
                    import warnings, traceback
                    warnings.warn(
                        'unable to transfer file %r for record %r to server %r\n%s' % (
                        f, dbrecord, server, traceback.format_exc()))
                    continue
            p = self.path(dbrecord, f)
            self._make_available(p, server=server)
            continue
        return


    def makedirs(self, dbrecord, server=None, subdir=None):
        p = self.path(dbrecord)
        if subdir:
            p = os.path.join(p, subdir)
        self._makedirs(p, server=server)


    def untar(self, tarfile, path, server=None):
        self._untar(tarfile, path, server)


    def is_available(self, dbrecord, filename=None, server=None, files=None):
        if files is None: files = []

        self._debug.log("called with dbrecord=%s,%s, filename=%s, server=%s, files=%s" % (dbrecord.getTableName(), dbrecord.id, filename, server and server.short_description or 'localhost', files))
        if filename and filename not in files:
            files.append(filename)
        if not files: files = _default_files(dbrecord)

        for filename in files:
            self._debug.log("checking file %s" % (filename,))
            p = self.path(dbrecord, filename)
            self._debug.log("its path is %s" % (p,))
            available = self._is_available(p, server=server)
            msg = 'File %s for dbrecord %s:%s is ' % (filename, dbrecord.__class__.__name__, dbrecord.id)
            if not available: msg += 'not '
            msg += 'available on %s.' % (server and server.short_description or "localhost",)
            self._debug.log(msg)
            
            if not available: return False
            continue
        
        return True


    def existssomewhere(self, dbrecord, filename=None):
        '''check if a file(directory) for a db record exists somewhere in
        the storage.
        
        dbrecord: database record
        filename: name of the file (directory) for the dbrecord
        '''
        p = self.path(dbrecord, filename)
        r = bool(self._find_node(p))
        if r: return r
        # if not found, try to search all the servers
        director = self.director
        from vnf.dom.Server import Server
        servers = director.clerk.db.query(Server).all()
        servers.append(None)
        for server in servers:
            if self.is_available(dbrecord, filename=filename, server=server):
                return True
            continue
        return False


    def path(self, dbrecord, filename=None):
        d = os.path.join(dbrecord.getTableName(), dbrecord.id)
        if filename:
            return os.path.join(d, filename)
        return d


    def abspath(self, dbrecord, filename=None, server=None):
        node = _node(server)
        return self._engine().abspath(self.path(dbrecord, filename), node)
    

    def _rename(self, path1, path2, server=None):
        node = _node(server)
        return self._engine().rename(path1, path2, node=node)


    def _copy(self, path1, path2, server=None):
        node = _node(server)
        return self._engine().copy(path1, path2, node=node)


    def _symlink(self, path1, path2, server=None):
        node = _node(server)
        return self._engine().symlink(path1, path2, node=node)


    def _remember(self, path, server=None):
        node = _node(server)
        return self._engine().remember(path, node=node)


    def _forget(self, path, server=None):
        node = _node(server)
        return self._engine().forget(path, node=node)


    def _remove(self, path, server=None):
        node = _node(server)
        return self._engine().remove(path, node=node)


    def _make_available(self, path, server=None):
        self._debug.log('trying to make %s available at %s' % (path, server))
        node = _node(server)
        return self._engine().make_available(path, node=node)


    def _makedirs(self, path, server=None):
        "Creates directory"
        node = _node(server)
        return self._engine().makedirs(path, node=node)


    def _untar(self, tarfile, path, server=None):
        "Extracts (untars) tarfile to the specified 'path'. 'server' parameter is not supported"
        node = _node(server)
        return self._engine().untar(tarfile, path, node=node)


    def _is_available(self, path, server=None):
        node = _node(server)
        return self._engine().is_available(path, node=node)


    def _find_node(self, path):
        return self._engine().find_node(path)


    def _configure(self):
        base._configure(self)
        self.dataroot = self.inventory.dataroot
        return
    
    
    def _init(self):
        base._init(self)


    def _engine(self):
        if not hasattr(self, '_dds'): 
            self._dds = self._createEngine()
        return self._dds


    def _createEngine(self):
        from dds import dds, node
        masternode = node(address='localhost', rootpath=self.dataroot)

        csaccessor = self.director.csaccessor
        def readfile(url):
            server, path = _decodeurl(url)
            if _islocal(server):
                return open(path).read()
            import tempfile
            d = tempfile.mkdtemp()
            csaccessor.getfile(server, path, d)
            filename = os.path.split(path)[1]
            ret = open(os.path.join(d, filename)).read()
            import shutil
            shutil.rmtree(d)
            return ret
            
        def writefile(url, content):
            server, path = _decodeurl(url)
            if _islocal(server):
                return open(path, 'w').write(content)
            import tempfile
            f = tempfile.mktemp()
            open(f, 'w').write(content)
            from vnf.dom.Server import LocalHost as localhost
            csaccessor.copyfile(localhost, f, server, path)
            os.remove(f)
            return

        def makedirs(url):
            server, path = _decodeurl(url)
            if _islocal(server):
                if os.path.exists(path): return
                return os.makedirs(path)
            cmd = 'mkdir -p %s' % path
            csaccessor.execute(cmd, server, '')
            return

        def rmdirs():
            "Recursively removes directory"
            pass


        def rename(path1, path2, surl):
            server = _decodesurl(surl)
            if _islocal(server):
                try:
                    return os.rename(path1, path2)
                except Exception, e:
                    msg = 'Unable to rename path %r to %r: %s' % (path1, path2, e)
                    raise RuntimeError, msg
            cmd = 'mv %s %s' % (path1, path2)
            csaccessor.execute(cmd, server, '')
            return

        def remove(path, surl):
            server = _decodesurl(surl)
            if _islocal(server):
                try:
                    return os.remove(path)
                except Exception, e:
                    msg = 'Unable to remove path %r.\n%s' % (path, e)
                    raise RuntimeError, msg
            cmd = 'rm %s' % (path,)
            csaccessor.execute(cmd, server, '')
            return

        def symlink(path1, path2, surl):
            server = _decodesurl(surl)
            if _islocal(server):
                try:
                    return os.symlink(path1, path2)
                except Exception, e:
                    msg = 'Unable to symlink path %r to %r: %s' % (path1, path2, e)
                    raise RuntimeError, msg
            cmd = 'ln -s %s %s' % (path1, path2)
            csaccessor.execute(cmd, server, '')
            return

        def fileexists(url):
            server, path = _decodeurl(url)
            self._debug.log('server=%r,path=%r'%(_surl(server),path))
            if _islocal(server):
                ret = os.path.exists(path)
            else:
                cmd = 'ls %s' % path
                self._debug.log('cmd=%r'%cmd)
                failed, out, err = csaccessor.execute(cmd, server, '', suppressException=True)
                if failed:
                    self._debug.log('cmd %r failed\n - out %s\n - error %s\n' % (
                            cmd, out, err))
                ret = not failed
                    
            msg = 'url %s does %s exist' % (url, not ret and 'not' or '')
            self._debug.log(msg)
            
            return ret
            
            
        def transferfile(url1, url2):
            server1, path1 = _decodeurl(url1)
            server2, path2 = _decodeurl(url2)
            if _islocal(server1) and _islocal(server2):
                self._debug.log('local copy: %s -> %s' % (path1, path2))
                import shutil
                shutil.copy(path1, path2)
                return
            csaccessor.copyfile(server1, path1, server2, path2)
            return
            
        self.masternode = masternode
        return dds(
            masternode=masternode,
            transferfile=transferfile,
            readfile=readfile, writefile=writefile, makedirs=makedirs,
            rename=rename, symlink=symlink, fileexists=fileexists,
            remove = remove,
            )

    pass # end of DistributedDataStorage


import os


def _default_files(dbrecord):
    try:
        return dbrecord.datafiles
    except AttributeError:
        return []


def _islocal(server):
    if server.username: return False
    address = server.address
    return server.port in [None, 22, '22'] and \
           (not address or address in ['localhost', '127.0.0.1'])

def _node(server):
    if server is None: return
    import dds
    return dds.node(
        address='%s@%s(%s)' % (server.username, server.address, server.port),
        rootpath = server.workdir)

def _decodeurl(url):
    #url: username@address(port):path
    splits = url.split(':')
    if len(splits)==1:
        s, path = '', url
    elif len(splits)==2:
        s, path = splits
    else:
        raise ValueError, url
    s = _decodesurl(s)
    return s, path

def _decodesurl(s):
    #url: username@address(port)
    if s.find('(')!=-1:
        a,p = s.split('(')
        p = p.strip()
        assert p[-1]==')'
        p = p[:-1]
    else:
        a = s
        p = 22
    port = p
    if a.find('@') == -1:
        username = ''; address = a
    else:
        username,address = a.split('@')

    if address == '': address = 'localhost'

    class Server:
        username = ''
        port = ''
        address = ''
        def __str__(self):
            return _surl(self)
        def __eq__(self, rhs):
            return self.username == rhs.username \
                   and self.port == rhs.port \
                   and self.address == rhs.address
    s = Server()
    s.username = username
    s.port = p
    s.address = address
    return s

def _surl(server):
    return '%s@%s(%s)' % (server.username, server.address, server.port)

def _files(dbrecord, files=None, filename=None):
    if files and filename:
        msg = "Both files and filename are supplied: files=%s, filename=%s" % (
            files, filename)
        raise ValueError, msg
    
    if filename:
        files = [filename]
    else:
        if not files:
            files = _default_files(dbrecord)
    return files
    


import os

# version
__id__ = "$Id$"

# End of file 
