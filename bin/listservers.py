#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.applications.UIApp import UIApp as base


class App(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk

        from vnf.dom.Server import Server
        servers = clerk.db.query(Server).all()

        for s in servers:
            print s.id
        return


    def __init__(self):
        base.__init__(self, 'listservers')
        return


    def _getPrivateDepositoryLocations(self):
        from vnf.deployment import pyre_depositories
        return pyre_depositories


import os, datetime


def main():
    import journal
    journal.debug('listservers').activate()
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
