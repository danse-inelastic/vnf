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
        self.dds.add_node(node)
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
            self._forget(path, server=server)
            continue
        return


    def move(self, dbrecord1, filename1, dbrecord2, filename2, server=None):
        path1 = self.path(dbrecord1, filename1)
        path2 = self.path(dbrecord2, filename2)
        return self._rename(path1, path2, server=server)


    def copy(self, dbrecord1, filename1, dbrecord2, filename2, server=None):
        path1 = self.path(dbrecord1, filename1)
        path2 = self.path(dbrecord2, filename2)
        return self._copy(path1, path2, server=server)


    def symlink(self, dbrecord1, filename1, dbrecord2, filename2, server=None):
        path1 = self.path(dbrecord1, filename1)
        path2 = self.path(dbrecord2, filename2)
        return self._symlink(path1, path2, server=server)


    def make_available(self, dbrecord, files=None, server=None):
        if files is None: files = _default_files(dbrecord)
        for f in files:
            p = self.path(dbrecord, f)
            self._make_available(p, server=server)
            continue
        return


    def is_available(self, dbrecord, filename, server=None):
        p = self.path(dbrecord, filename)
        return self._is_available(p, server=server)


    def path(self, dbrecord, filename=None):
        d = os.path.join(dbrecord.name, dbrecord.id)
        if filename: return os.path.join(d, filename)
        return d


    def abspath(self, dbrecord, filename=None, server=None):
        node = _node(server)
        return self.dds.abspath(self.path(dbrecord, filename), node)
    

    def _rename(self, path1, path2, server=None):
        node = _node(server)
        return self.dds.rename(path1, path2, node=node)


    def _copy(self, path1, path2, server=None):
        node = _node(server)
        return self.dds.copy(path1, path2, node=node)


    def _symlink(self, path1, path2, server=None):
        node = _node(server)
        return self.dds.symlink(path1, path2, node=node)


    def _remember(self, path, server=None):
        node = _node(server)
        return self.dds.remember(path, node=node)


    def _forget(self, path, server=None):
        node = _node(server)
        return self.dds.forget(path, node=node)


    def _make_available(self, path, server=None):
        node = _node(server)
        return self.dds.make_available(path, node=node)


    def _is_available(self, path, server=None):
        node = _node(server)
        return self.dds.is_available(path, node=node)


    def _configure(self):
        base._configure(self)
        self.dataroot = self.inventory.dataroot
        return
    
    
    def _init(self):
        base._init(self)

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
            shutil.rmtree(d)
            return ret
            
        def writefile(url, content):
            server, path = _decodeurl(url)
            if _islocal(server):
                return open(path, 'w').write(content)
            import tempfile
            f = tempfile.mktemp()
            open(f, 'w').write(content)
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
                return os.path.exists(path)
            cmd = 'ls %s' % path
            self._debug.log('cmd=%r'%cmd)
            failed, out, err = csaccessor.execute(cmd, server, '', suppressException=True)
            return not failed
            
            
        def transferfile(url1, url2):
            server1, path1 = _decodeurl(url1)
            server2, path2 = _decodeurl(url2)
            if _islocal(server1) and _islocal(server2):
                import shutil
                shutil.copy(path1, path2)
                return
            csaccessor.copyfile(server1, path1, server2, path2)
            return
            
        self.masternode = masternode
        self.dds = dds(
            masternode=masternode,
            transferfile=transferfile,
            readfile=readfile, writefile=writefile, makedirs=makedirs,
            rename=rename, symlink=symlink, fileexists=fileexists,
            )

        return

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
