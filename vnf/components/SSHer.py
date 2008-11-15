# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from CSAccessor import CSAccessor as base, RemoteAccessError

class SSHer(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        #auth_sock = pyre.inventory.str( 'auth_sock')
        known_hosts = pyre.inventory.str( 'known_hosts' )
        private_key = pyre.inventory.str( 'private_key' )

        pass # end of Inventory
    

    def __init__(self, *args, **kwds):
        base.__init__(self, *args, **kwds)
        return


    def copyfile(self, server1, path1, server2, path2):
        'copy recursively from server1 to server2'
        if not _localhost(server1) and not _localhost(server2):
            return self._copyfile_rr(server1, path1, server2, path2)
        if _localhost(server1) and _localhost(server2):
            import shutil
            shutil.copy(path1, path2)
        if _localhost(server1): self._copyfile_lr(path1, server2, path2)
        if _localhost(server2): self.getfile(server1, path1, os.path.split(path2)[0] or '.')
        return
    

    def pushdir( self, path, server, remotepath ):
        'push a local directory to remote server'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            ]

        if port:
            pieces.append( '-P %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '-r %s' % path,
            '%s@%s:%s' % (username, address, remotepath),
            ]

        cmd = ' '.join(pieces)
        
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    def getfile( self, server, remotepath, localdir ):
        'retrieve file from remote server to local path'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key
        
        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            ]
        
        if port:
            pieces.append( '-P %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '-r',
            '%s@%s:%s' % (username, address, remotepath),
            '%s' % localdir,
            ]

        cmd = ' '.join(pieces)
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg

        remotedir, filename = os.path.split( remotepath )
        return os.path.join( localdir, filename )


    def execute( self, cmd, server, remotepath, suppressException = False ):
        'execute command in the given directory of the given server'

        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        rmtcmd = 'cd %s && %s' % (remotepath, cmd)
        
        pieces = [
            'ssh',
            "-o 'StrictHostKeyChecking=no'",
            ]
        
        if port:
            pieces.append( '-p %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )

        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s' % (username, address),
            '"%s"' % rmtcmd,
            ]

        cmd = ' '.join(pieces)

        self._info.log( 'execute: %s' % cmd )
        failed, output, error = spawn( cmd )
        if failed and not suppressException:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return failed, output, error


    def _copyfile_rr(self, server1, path1, server2, path2):
        address2 = server2.address
        port2 = server2.port
        username2 = server2.username

        pieces = [
            'scp',
            '-P %s' % port2,
            '-r %s' % path1,
            '%s@%s:%s' % (username2, address2, path2),
            ]

        cmd = ' '.join(pieces)
        
        self.execute(cmd, server1, '')
        return
    

    def _copyfile_lr( self, path, server, remotepath ):
        'push a local file to remote server'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            ]
        
        if port:
            pieces.append( '-P %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )

        if private_key:
            pieces.append( "-i %s" % private_key )

        pieces += [
            path,
            '%s@%s:%s' % (username, address, remotepath),
            ]

        cmd = ' '.join(pieces)
        
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    pass # end of SSHer



def _localhost(server):
    address = server.address
    port = server.port
    return (port in [None, 22, '22']) and (address in [None, 'localhost', '127.0.0.1'])


import os
from spawn import spawn


# version
__id__ = "$Id$"

# End of file 
