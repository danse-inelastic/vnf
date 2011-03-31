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


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        outputdir = pyre.inventory.str(name='outputdir', default='db-pickle')

        tables = pyre.inventory.list(name='tables')


    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        clerk.importAllDataObjects()

        tables = self.inventory.tables
        if not tables:
            tables = list(clerk.db.iterAllTables())
        else:
            tables = map(clerk._getTable, tables)
        
        from dsaw.db.Pickler import Pickler
        outputdir = self.inventory.outputdir
        pickler = Pickler(clerk.db, outputdir)
        pickler.dump(tables=tables)
        return


    def __init__(self):
        base.__init__(self, 'dumpdb')
        return


    def _defaults(self):
        super(DbApp, self)._defaults()
        from vnf.components.Clerk import Clerk
        self.inventory.clerk = Clerk()
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config']



def main():
    import journal
    journal.debug('db').activate()
    app = DbApp()
    return app.run()


# main
if __name__ == '__main__':
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
