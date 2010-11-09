# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def check(server, csaccessor):
    for package, cmds in commands.iteritems():
        for cmd in cmds:
            checkPackage(package, cmd, server, csaccessor)
        continue
    return


def checkPackage(package, testcmd, server, csaccessor):
    print 'checking package %r by running command %r' % (
        package, testcmd)
    failed, out, err = csaccessor.execute(testcmd, server, '/tmp', suppressException=True)
    if failed:
        print '* FAIELD!'
        print '* OUTPUT: %s\n\n' % out
        print '* ERROR: %s\n\n' % err
    
    else:
        print '* SUCCEED'
    return


commands = {
    'mcvine': [
        '. ~/.mcvine && python -c "import mcvine"',
        '''. ~/.mcvine && mpirun -np 2 '`which mpipython.exe` -c "import mpi; print mpi.world().rank"' ''',
        ],
    'bvk': [
        '. ~/.bvk && python -c "import bvk"',
        ]
    }


# version
__id__ = "$Id$"

# End of file 
