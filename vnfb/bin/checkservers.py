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

        from vnfb.dom.Server import Server
        servers = clerk.db.query(Server).filter_by(status='online').all()
        
        map(self._check, servers)
        return


    def _check(self, server):
        print "checking server %r ..." % server.short_description
        csa = self.csaccessor
        failed, output, error = csa.execute('ls', server, '/tmp', suppressException=True)
        if failed:
            self._offline(server, error)
        return


    def _offline(self, server, error):
        db = self.clerk.db

        server.status = 'offline'
        db.updateRecord(server)

        from vnfb.utils.communications import announce
        announce(self, 'computing-server-down', server, error)
        return


    def __init__(self):
        base.__init__(self, 'checkservers')
        return


    def _getPrivateDepositoryLocations(self):
        from vnfb.deployment import pyre_depositories
        return pyre_depositories



def main():
    import journal
    journal.debug('checkservers').activate()
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
