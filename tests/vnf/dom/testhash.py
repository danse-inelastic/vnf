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



from pyre.applications.Script import Script


class App(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        table = pyre.inventory.str(name='table', default='table')
        id = pyre.inventory.str(name='id', default='')


    def main(self, *args, **kwds):
        record = self.clerk.getRecordByID(self.table, self.id)
        from vnf.dom.hash import hash
        db = self.clerk.db
        print hash(record, db)
        return


    def __init__(self):
        Script.__init__(self, 'checkdb')
        self.db = None
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self

        self.table = self.inventory.table
        self.id = self.inventory.id
        return


    def _init(self):
        Script._init(self)

        self.db = self.clerk.db

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']
    


def main():
    import journal
    #journal.debug('db').activate()
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
