#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.applications.Script import Script as base

class EstablishGlobalPointers(base):

    class Inventory(base.Inventory):

        import pyre.inventory

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        tables = pyre.inventory.list(name='tables', default=[])
        skip_tables = pyre.inventory.list(name='skip-tables', default=[])

        pass # end of Inventory
        

    def main(self):
        db = self.clerk.db
        
        tables = self.inventory.tables
        skip_tables = self.inventory.skip_tables

        if tables and skip_tables: raise RuntimeError

        from vnf.dom import alltables
        alltables = alltables()
        if tables:
            tables = map(db.getTable, tables)
        elif skip_tables:
            skip_tables = map(db.getTable, skip_tables)
            tables = filter(lambda t: t not in skip_tables, alltables)
        else:
            tables = alltables

        from dsaw.db.GloballyReferrable import GloballyReferrable
        tables = filter(lambda t: issubclass(t, GloballyReferrable), tables)

        for table in tables:
            records = db.fetchall(table)
            for r in records:
                if r.globalpointer is None or not r.globalpointer.id:
                    r.establishGlobalPointer(db)
            continue
        
        return


    def _configure(self):
        base._configure(self)

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)
        return


import os    

# version
__id__ = "$Id$"

# End of file 
