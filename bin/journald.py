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


def main():


    from journal.services.Daemon import Daemon


    class JournaldApp(Daemon):


        def _defaults(self):
            Daemon._defaults(self)
            self.inventory.client = "remote"
            return


        def _getPrivateDepositoryLocations(self):
            return ['../config']


    app = JournaldApp()
    return app.run(spawn=True)


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id: journald.py,v 1.1.1.1 2006-11-27 00:09:14 aivazis Exp $"

# End of file 
