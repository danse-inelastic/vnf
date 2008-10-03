#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                      California Institute of Technology
#                      (C) 1998-2005  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def main(depositoryLocation='../config'):


    from journal.services.Daemon import Daemon


    class JournaldApp(Daemon):


        def _defaults(self):
            Daemon._defaults(self)
            self.inventory.client = "remote"
            return


        def _getPrivateDepositoryLocations(self):
            print 'using '+depositoryLocation+' as a depository'
            return [depositoryLocation]


    app = JournaldApp()
    return app.run(spawn=True)


# main
if __name__ == '__main__':
    # invoke the application shell
    import sys
    if sys.argv[1]:
        main(sys.argv[1])
    else:
        main()


# version
__id__ = "$Id: journald.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
