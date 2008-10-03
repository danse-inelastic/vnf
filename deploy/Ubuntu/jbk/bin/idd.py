#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Michael A.G. Aivazis
#                        California Institute of Technology
#                        (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main(depositoryLocation='../config'):


    from pyre.idd.Daemon import Daemon


    class IDDdApp(Daemon):


        def _getPrivateDepositoryLocations(self):
            print 'using '+depositoryLocation+' as a depository'
            return [depositoryLocation]


    app = IDDdApp()
    return app.run(spawn=True)


# main
if __name__ == '__main__':
    # invoke the application shell
    import sys
    if len(sys.argv)>1:
        main(sys.argv[1])
    else:
        main()


# version
__id__ = "$Id: idd.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
