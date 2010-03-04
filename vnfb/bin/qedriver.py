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

# Let there be light ... from the darkness of messy code! :)
# If everyone is reinventing the wheel, why not to join them? :)

def main():
    from vnfb.applications.QEDriver import QEDriver

    class App(ITaskApp):

        def _getPrivateDepositoryLocations(self):
            return ['/tmp/luban-services', '../config', '../content/components']

    app = App()
    return app.run()

# main
if __name__ == '__main__':
    # invoke the application shell
    main()

__date__ = "$Mar 3, 2010 10:57:53 PM$"


