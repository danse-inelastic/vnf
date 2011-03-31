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
        id = pyre.inventory.str('id')


    def help(self):
        print 'activateserver.py --id=<server_id>'
        return


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk

        from vnfb.dom.Server import Server
        id = self.inventory.id
        server = clerk.getRecordByID(Server, id)

        failed = self._check(server)
        if failed: return

        self._activate(server)
        return


    def _check(self, server):
        csa = self.csaccessor
        failed, output, error = csa.execute('ls', server, '/tmp', suppressException=True)
        if failed:
            print 'check server %r failed: %s' % (server.short_description, error)
        return failed


    def _activate(self, server):
        db = self.clerk.db

        server.status = 'online'
        db.updateRecord(server)

        print "server %s activated" % server.short_description
        # from vnfb.utils.communications import announce
        # announce(self, 'computing-server-activated', server, error)
        return


    def __init__(self):
        base.__init__(self, 'activateserver')
        return


    def _getPrivateDepositoryLocations(self):
        from vnfb.deployment import pyre_depositories
        return pyre_depositories



def main():
    import journal
    journal.debug('activateserver').activate()
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
