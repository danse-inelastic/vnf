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
    

    def remember(self, path, server=None):
        node = _node(server)
        return self.dds.remember(path, node=node)


    def make_available(self, path, server=None):
        node = _node(server)
        return self.dds.make_available(path, node=node)


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
            csaccessor.execute(server, cmd, '')
            return

        def fileexists(url):
            server, path = _decodeurl(url)
            if _islocal(server):
                return os.path.exists(path)
            cmd = 'ls %s' % path
            failed, out, err = csaccessor.execute(server, cmd, '')
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
            
        
        self.dds = dds(
            masternode=masternode,
            transferfile=transferfile,
            readfile=readfile, writefile=writefile, makedirs=makedirs,
            fileexists=fileexists)

        return

    pass # end of DistributedDataStorage


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
    s, path = url.split(':')
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

    class Server: pass
    s = Server()
    s.username = username
    s.port = p
    s.address = address
    return s, path


import os

# version
__id__ = "$Id$"

# End of file 
