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
            "-o 'UserKnownHostsFile=%s'" % known_hosts,
            '-P %s' % port,
            ]
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '-r %s' % path,
            '%s@%s:%s' % (username, address, remotepath),
            ]

        cmd = ' '.join(pieces)
        
        self._info.log( 'execute: %s' % cmd )

        env = {
            }
        failed, output, error = spawn( cmd, env = env )
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
            "-o 'UserKnownHostsFile=%s'" % known_hosts,
            '-P %s' % port,
            ]
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s:%s' % (username, address, remotepath),
            '%s' % localdir,
            ]

        cmd = ' '.join(pieces)
        self._info.log( 'execute: %s' % cmd )

        env = {}
        failed, output, error = spawn( cmd, env = env )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg

        remotedir, filename = os.path.split( remotepath )
        return os.path.join( localdir, filename )


    def execute( self, cmd, server, remotepath ):
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
            "-o 'UserKnownHostsFile=%s'" % known_hosts,
            '-p %s' % port,
            ]
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s' % (username, address),
            '"%s"' % rmtcmd,
            ]

        cmd = ' '.join(pieces)

        self._info.log( 'execute: %s' % cmd )
        env = {
            }
        failed, output, error = spawn( cmd, env = env )
        return failed, output, error


    pass # end of SSHer


import os
from spawn import spawn


# version
__id__ = "$Id$"

# End of file 
