#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def main():
    from vnfb.applications.ConvJobDriver import ConvJobDriver

    class App(ConvJobDriver):

        def _getPrivateDepositoryLocations(self):
            return ['/tmp/luban-services', '../config', '../content/components']

    app = App()
    return app.run()

# main
if __name__ == '__main__':
    # invoke the application shell
    main()

__date__ = "$May 2, 2010 3:51:09 PM$"


