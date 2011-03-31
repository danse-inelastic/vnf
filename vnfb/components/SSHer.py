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
        user = pyre.inventory.str('user', default = 'www-data')
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
        if _localhost(server2):
            if os.path.isdir(path2):
                dir = path2; newfilename = None
            else:
                dir = os.path.dirname(path2); newfilename = os.path.basename(path2)
            self.getfile(server1, path1, localdir=dir, newfilename=newfilename)
        return
    

    def pushdir( self, path, server, remotepath ):
        '''push a local directory to remote server

    Eg:
        pushdir('/a/b/c', server1, '/a1/b1'): directory /a/b/c will be copied to server1 and become /a1/b1/c
        '''
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key

        # tar -czf - <sourcepath> | ssh <remotehost> "(cd <remotepath>; tar -xzf -)"
        pieces = [
            'tar',
            '-czf',
            '-',
            path,
            '|',
            'ssh',
            "-o 'StrictHostKeyChecking=no'",
            "-o 'BatchMode=yes'",
            ]

        if port:
            pieces.append( '-p %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )
        
        if private_key:
            pieces.append( "-i %s" % private_key )
            
        pieces += [
            '%s@%s' % (username, address),
            '"(cd %s; tar -xzf -)"' % remotepath,
            ]

        cmd = ' '.join(pieces)
        
        self._info.log( 'execute: %s' % cmd )

        failed, output, error = spawn( cmd )
        
        self._info.log( 'spawn: failed: %s; output: %s; error: %s' % (failed, output, error) )
        
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return


    def getfile( self, server, remotepath, localdir, newfilename=None):
        'retrieve file from remote server to local path'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key
        
        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            "-o 'BatchMode=yes'",
            ]
        
        if port:
            pieces.append( '-P %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )
        
        if private_key:
            pieces.append( "-i %s" % private_key )

        localpath = localdir
        if newfilename:
            localpath = os.path.join(localdir, newfilename)
        pieces += [
            '%s@%s:%s' % (username, address, remotepath),
            '%s' % localpath,
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


    def getdirectory( self, server, remotepath, localdir ):
        'retrieve a directory from remote server to local path'
        address = server.address
        port = server.port
        username = server.username
        known_hosts = self.inventory.known_hosts
        private_key = self.inventory.private_key
        
        pieces = [
            'scp',
            "-o 'StrictHostKeyChecking=no'",
            "-o 'BatchMode=yes'",
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

        # Escaping " (and \") character from cmd string:
        cmd     = cmd.replace('\\\"', '"')  # Make sure that there are no already escaped "
        cmd     = cmd.replace('"', '\\\"')
        rmtcmd  = 'cd %s && %s' % (remotepath, cmd)
        
        if private_key:
            socket, pid = self._create_agent_with_key(private_key)

        pieces = []

        if private_key:
            pieces += ['SSH_AUTH_SOCK=%s' % socket]

        pieces += [
            'ssh',
            "-o 'StrictHostKeyChecking=no'",
            "-o 'BatchMode=yes'",
            "-A", 
            ]
        
        if port:
            pieces.append( '-p %s' % port )

        if known_hosts:
            pieces.append( "-o 'UserKnownHostsFile=%s'" % known_hosts )

        # if private_key:
        #    pieces.append( "-i %s" % private_key )
            
        if username:
            pieces.append('%s@%s' % (username, address))
        else:
            pieces.append('%s' % (address,))
        pieces += [
            '"%s"' % rmtcmd,    # Fixed "" can be a problem
            ]


        cmd = ' '.join(pieces)

        self._info.log( 'execute: %s' % cmd )
        failed, output, error = spawn( cmd )

        if private_key:
            self._kill_agent(pid)

        if failed and not suppressException:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RemoteAccessError, msg
        return failed, output, error


    def _create_agent(self):
        cmd = 'eval `ssh-agent`  > /dev/null; echo $SSH_AUTH_SOCK; echo $SSH_AGENT_PID'
        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RuntimeError, msg
        lines = output.splitlines()
        socket = lines[0].strip()
        pid = lines[1].strip()
        return socket, pid
    

    def _create_agent_with_key(self, private_key):
        socket, pid = self._create_agent()
        cmd = 'SSH_AUTH_SOCK=%s ssh-add "%s" > /dev/null; ' % (
            socket, private_key)
        failed, output, error = spawn( cmd )
        if failed:
            self._kill_agent(pid)
            msg = '%r failed: %s' % (
                cmd, error )
            raise RuntimeError, msg
        return socket, pid


    def _kill_agent(self, pid):
        cmd = 'kill -9 %s' % pid
        failed, output, error = spawn( cmd )
        if failed:
            msg = '%r failed: %s' % (
                cmd, error )
            raise RuntimeError, msg
        return


    def _isdirectory(self, server, path):
        if _localhost(server):
            return os.path.isdir(path)
        cmd = '''python -c "import os; print int(os.path.isdir('%s'))"''' % path
        failed, out, err = self.execute(cmd, server, '')
        return int(out)
        
        
    def _copyfile_rr(self, server1, path1, server2, path2):
        'push a remote file to another remote server'
        # basic idea is to ssh into a remote host (server1 or server2)
        # and run a scp command there.
        # this assumes that scp is available on that host
        # "rhost" will be the chosen remote host

        def url(server, path):
            rt = '%s@%s:%s/%s' % (
                server.username, server.address, server.port, path)
            if self._isdirectory(server, path):
                rt += '/'
            return rt

        if not path1.endswith('/') and self._isdirectory(server1, path1):
            path1 += '/'
        if not path2.endswith('/') and self._isdirectory(server2, path2):
            path2 += '/'

        if server1 == server2:
            pieces = [
                'rsync -a',
                path1,
                path2,
                ]
            rhost = server1

        elif _tunneled_remote_host(server1) and _tunneled_remote_host(server2):
            raise NotImplementedError, 'server1: %s, server2: %s' % (server1, server2)

        # the implementation here is not the best. We should have used rsync
        # but rsync does not work with tunneled ssh port directly (could use
        # rsync port but that is no guarantee).
        elif not _tunneled_remote_host(server2):
            # server2 is not tunneled and universally accessible
            # so we can ssh to server1 and then scp to server2
            address2 = server2.address
            port2 = server2.port
            username2 = server2.username

            pieces = [
                'scp -r',
                ]
            if port2:
                pieces.append('-P %s' % port2)
            pieces.append('-r %s' % path1)
            pieces.append('%s@%s:%s' % (username2, address2, path2))
            rhost = server1

        else:
            # server2 is tunneled
            # we need to ssh to server2 and get stuff from server1
            address1 = server1.address
            port1 = server1.port
            username1 = server1.username
            
            pieces = [
                'scp -r',
                ]
            if port1:
                pieces.append('-P %s' % port1)
            pieces.append('%s@%s:%s' % (username1, address1, path1))
            pieces.append('%s' % path2)
            rhost = server2

        cmd = ' '.join(pieces)
        
        self.execute(cmd, rhost, '')
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
            "-o 'BatchMode=yes'",
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


_localhost_aliases = [
    None, 'localhost', '127.0.0.1',
    ]
_localport_aliases = [
    None, 22, '22',
    ]
def _localhost(server):
    address = server.address
    port = server.port
    return (port in _localport_aliases) and (address in _localhost_aliases)
def _tunneled_remote_host(server):
    address = server.address
    if address not in _localhost_aliases: return False
    port = server.port
    return port not in _localport_aliases


import os
from vnf.utils.spawn import spawn


# version
__id__ = "$Id$"

# End of file 
