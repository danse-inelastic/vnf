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

        inputdir = pyre.inventory.str(name='inputdir', default='db-pickle')
        
        
    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        clerk.importAllDataObjects()

        tables = list(clerk.db.iterAllTables())
        
        from dsaw.db.Unpickler import Unpickler
        inputdir = self.inventory.inputdir
        unpickler = Unpickler(clerk.db, inputdir)
        unpickler.load(tables)
        return


    def __init__(self):
        base.__init__(self, 'restoredb')
        return


    def _defaults(self):
        super(DbApp, self)._defaults()
        from vnfb.components.Clerk import Clerk
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
