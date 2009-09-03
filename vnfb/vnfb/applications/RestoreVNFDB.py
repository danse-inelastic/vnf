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

class RestoreVNFDB(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        srcdir = pyre.inventory.str('srcdir')

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", default='clerk')
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        tables = pyre.inventory.list(name='tables', default=[])
        skip_tables = pyre.inventory.list(name='skip-tables', default=[])

        idonly = pyre.inventory.bool(name='idonly', default=True)
        update = pyre.inventory.bool(name='update', default=True)

        pass # end of Inventory
        

    def main(self):
        tables = self.inventory.tables
        skip_tables = self.inventory.skip_tables
        
        db = self.clerk.db
        srcdir = self.srcdir

        from dsaw.db import restore
        
        import os
        records_strings = {}
        for entry in os.listdir(srcdir):
            path = os.path.join(srcdir, entry)
            s = open(path).read()
            
            tablename = entry
            if tables and tablename not in tables or tablename in skip_tables: continue
            
            table = db.getTable(tablename)

            records_strings[table] = s
            continue

        if self.inventory.idonly:
            for table, s in records_strings.iteritems():
                print 'Establishing records (id only) for table %s...' % table.name
                restore.loads(s, db, table, idonly=True, update=False)
                continue
            
        if self.inventory.update:
            for table, s in records_strings.iteritems():
                print 'Updating records for table %s...' % table.name
                failed = restore.loads(s, db, table, idonly=False, update=True)

                for row, reason in failed:
                    print 'Failed to insert row %s, reason: %s' %(row.id, reason)
                continue
            
        return


    def _configure(self):
        base._configure(self)

        self.srcdir = self.inventory.srcdir

        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)

        if not os.path.exists(self.srcdir):
            raise RuntimeError, '%s does not exist' % self.srcdir

        return


import os    

# version
__id__ = "$Id$"

# End of file 
