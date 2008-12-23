#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


## Check if the db has the necessary tables for vnf to run


from pyre.applications.Script import Script


class App(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        tables = pyre.inventory.list(name='tables', default=[])


    def main(self, *args, **kwds):

        self.db.autocommit(True)

        tables = self.tables
        if not tables:
            from vnf.dom import alltables
            tables = alltables()
        else:
            tables = [self.clerk._getTable(t) for t in tables]

        from vnf.dom.check import issane
        for table in tables:
            print '* checking', table.name
            if not issane(table, self.db): print ' '*4, '*** error'
            continue
        return


    def __init__(self):
        Script.__init__(self, 'checkdb')
        self.db = None
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        self.tables = self.inventory.tables
        return


    def _init(self):
        Script._init(self)

        self.db = self.clerk.db
        self.idd = self.inventory.idd

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # id generator
        def guid(): return '%s' % self.idd.token().locator
        import vnf.dom
        vnf.dom.set_idgenerator( guid )
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']
    


def main():
    import journal
    #journal.debug('db').activate()
    journal.info('vnf.dom.check').activate()
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
