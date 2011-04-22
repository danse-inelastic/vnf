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
    dry_run: if true, only print the command to be executed
    
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
    
    p = subprocess.Popen(
        cmd, 
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE,
        shell = True, env = env,
        )
    
    out, err = p.communicate()
    ret = p.wait()
    # 
    del p

    info.log( "cmd \n%s\n finished" % cmd )
    return ret, out, err
import types


def test_spawn( ):
    print spawn( 'ls' )
    return


def test():
    test_spawn()
    return


if __name__ == '__main__': test()



# version
__id__ = "$Id$"

# End of file 
