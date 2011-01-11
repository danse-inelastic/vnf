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

        strategy = pyre.inventory.str(
            name='strategy', default='', 
            validator=pyre.inventory.choice(['', 'overwrite', 'skip', 'prompt'])
            )

        idcol = pyre.inventory.str('idcol', default='id')
        
        tables = pyre.inventory.list(name='tables')


    def help(self):
        import sys
        cmdname = sys.argv[0]
        print '-'*70
        print "Restore db from files saved by dumpdb.py" 
        print '-'*70
        print '%s -inputdir=<input-data-directory> -strategy=<strategy> -tables=<tables> -idcol=<idcol>' % cmdname
        print
        print " --strategy: strategy of restoring when records already exist"
        print "   * overwrite"
        print "   * skip"
        print "   * prompt"
        print 
        print " --idcol: name of the column that is the primary key. by default it is 'id'"
        print 
        print '-'*70
        
        
    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        clerk.importAllDataObjects()

        tables = self.inventory.tables
        if not tables:
            tables = list(clerk.db.iterAllTables())
        else:
            tables = map(clerk._getTable, tables)
        
        from dsaw.db.Unpickler import Unpickler
        inputdir = self.inventory.inputdir
        unpickler = Unpickler(clerk.db, inputdir)

        strategy = self.inventory.strategy or None
        idcol = self.inventory.idcol
        unpickler.load(tables, strategy=strategy, idcol=idcol)
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
