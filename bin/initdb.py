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



"""
initialized database with data objects loaded
"""


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        table = pyre.inventory.str(name='table')
        tables = pyre.inventory.list(name='tables')
        

    def main(self, *args, **kwds):
        clerk = self.clerk
        clerk.importAllDataObjects()
        print "registered tables:"
        for table in clerk.db.iterAllTables():
            print ' -', table.getTableName()
        print
        print "create all tables"
        clerk.db.createAllTables()
        
        tables = self.inventory.tables
        if not tables:
            table = self.inventory.table
            if table:
                tables = [table]

        print "init tables"
        self.inittables(tables)
        return


    def inittables(self, tables):
        map(self.inittable, tables)


    def inittable(self, table):
        print ' * %s' % table
        clerk = self.inventory.clerk
        orm = clerk.orm

        component = self.retrieveInitalizer(table)
        if hasattr(component, 'getObjects'):
            objs = component.getObjects()
            for obj in objs:
                orm.save(obj)

        elif hasattr(component, 'initdb'):
            component.initdb()

        elif component is None:
            print 'initdb component for table %s does not exist' % table
            pass

        else:
            raise RuntimeError, 'initdb component for table %s does not implement the required interface' % table

        return


    def retrieveInitalizer(self, name):
        component = self.retrieveComponent(name, factory='initdb', vault=['initdb'])
        if component is None:
            curator_dump = self._dumpCurator()
            self._debug.log("could not locate db initializer %r. curator dump: %s" % (
                name, curator_dump))
        else:
            self.configureComponent(component)
            component.director = self
        return component


    def __init__(self):
        base.__init__(self, 'initdb')
        return


    def _getPrivateDepositoryLocations(self):
        return ['../config', '../content/components', '/tmp/luban-services']



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
