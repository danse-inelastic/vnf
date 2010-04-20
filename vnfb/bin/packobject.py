#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def main():

    from vnfb.applications.PackObject import PackObject as base

    class App(base):
        def _getPrivateDepositoryLocations(self):
            return ['../config']


    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
