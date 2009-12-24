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


# find all objects that referred to the given data object


from luban.applications.UIApp import UIApp as base


class DbApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        type = pyre.inventory.str(name='type')
        id = pyre.inventory.str(name='id')
        

    def main(self, *args, **kwds):
        clerk = self.inventory.clerk
        clerk.importAllDataObjects()
        
        type = self.inventory.type
        type = clerk._getObjectByImportingFromDOM(type)
        
        id = self.inventory.id

        orm = clerk.orm
        obj = orm.load(type, id)

        Obj = obj.__class__
        Table = orm(Obj)
        record = orm(obj)

        # find all talbes that could refer to this record
        print 'Gather references'
        refs = []; vrefs = []
        from dsaw.db.Reference import Reference
        from dsaw.db.VersatileReference import VersatileReference
        for Table1 in orm.db.iterAllTables():
            print ' * on table %s' % Table1.getTableName()
            if Table1 is Table: continue
            for name, col in Table1._columnRegistry.iteritems():
                if isinstance(col, Reference) and col.referred_table is Table:
                    refs.append((Table1, col))
                elif isinstance(col, VersatileReference):
                    vrefs.append((Table1, col))
            continue

        db = orm.db
        # for reference, we need to search the table
        print 'In References'
        refrecords = []
        for Table1, col in refs:
            print ' * searching ', Table1.getTableName(), col.name, '...'
            where = "%s='%s'" % (col.name, record.id)
            refrecords += db.query(Table1).filter(where).all()
            continue

        # for versatile reference, we need to search thru global pointer
        print 'In Polymorphic References'
        gp = record.globalpointer and record.globalpointer.id
        if gp:
            for Table1, col in vrefs:
                print ' * searching ', Table1.getTableName(), col.name, '...'
                where = "%s='%s'" % (col.name, gp)
                refrecords += db.query(Table1).filter(where).all()
                continue

        # report
        print
        print '*'*10, 'report', '*'*10
        print 'following are entities that refers to %s(%s):' % (Table.getTableName(), record.id)
        from dsaw.db._referenceset import _ReferenceSetTable
        refsettablename = _ReferenceSetTable.getTableName()
        for r in refrecords:
            tname = r.getTableName()
            if tname == refsettablename:
                container = r.container.dereference(db)
                
                # when this is a reference set where the interested object is the container,
                # skip
                if container.__class__ is Table and container.id == record.id:
                    continue
                
                element = r.element.dereference(db)
                print ' - refset %s: %s(%s).%s#%s %s %s(%s)' % (
                    r.id,
                    container.getTableName(), container.id,
                    r.containerlabel,
                    r.elementindex,
                    r.elementlabel,
                    element.getTableName(), element.id,
                    )
            else:
                print ' -', r.getTableName(), r.id
        return


    def __init__(self):
        base.__init__(self, 'findreferences')
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
