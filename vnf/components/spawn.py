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


import journal
info = journal.info( 'spawn' )


def spawn(command, dry_run = 0, env = None):
    """
    command: command to run
    env: environment variables to pass to the process in which the command will be executed
    dry_run: if true, only print the command to be excuted
    
    return: fail(bool), out(str), error(str)
    """

    if type(command) == list:
        cmd = ' '.join(command)
    else:
        assert(type(command) == types.StringType)
        cmd = command
        pass

    if dry_run:
        info.log( "Command to execute: \n%s" % cmd )
        return 

    info.log( "Executing: \n%s" % cmd )

    import subprocess
    import tempfile
    log = OStrStream()
    errlog = OStrStream()
    
    p = subprocess.Popen(
        cmd, stdout = log, stderr = errlog, shell = True, env = env)
    
    ret = p.wait()
    del p

    return ret, log.str(), errlog.str()
import types


class OStrStream:

    def __init__(self):
        import tempfile
        f = self.__filepath__ = tempfile.mktemp()
        self.__stream__ = open( f, 'w' )
        return


    def __del__(self):
        del self.__stream__
        import os
        os.remove( self.__filepath__ )
        return


    def __getattr__(self, name):
        return getattr(self.__stream__, name)
    

    def str(self):
        self.__stream__.close()
        s = open(self.__filepath__).read()
        return s

    pass # end of OStrStream


def test_spawn( ):
    print spawn( 'ls' )
    return


def test_OStrStream():
    oss = OStrStream()
    print >> oss, "hello"
    assert oss.str() == 'hello\n'
    return


def test():
    test_OStrStream()
    test_spawn()
    return


if __name__ == '__main__': test()



# version
__id__ = "$Id$"

# End of file 
