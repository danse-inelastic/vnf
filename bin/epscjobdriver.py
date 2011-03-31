#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

def main():
    from vnf.applications.EPSCJobDriver import EPSCJobDriver

    class App(EPSCJobDriver):

        def _getPrivateDepositoryLocations(self):
            return ['/tmp/luban-services', '../config', '../content/components']

    app = App()
    return app.run()

# main
if __name__ == '__main__':
    # invoke the application shell
    main()
    
__date__ = "$Mar 24, 2011 6:22:16 PM$"


