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

class MigrateTable(base):

    class Inventory(base.Inventory):

        import pyre.inventory
        table = pyre.inventory.str('table')
        oldtableurl = pyre.inventory.str('oldtableurl')

        import pyre.idd
        idd = pyre.inventory.facility('idd-session', factory=pyre.idd.session, args=['idd-session'])
        idd.meta['tip'] = "access to the token server"

        import vnf.components
        clerk = pyre.inventory.facility(name="clerk", factory=vnf.components.clerk)
        clerk.meta['tip'] = "the component that retrieves data from the various database tables"

        pass # end of Inventory
        

    def main(self):
        new = self.migrateRecords()
        self.dropTable(self.oldtable)
        self.createTable(self.table)
        for r in new: self.clerk.newRecord(r)
        return


    def createTable(self, table):
        # create the component table
        print " -- creating table %r" % table.name
        self.clerk.db.createTable(table)
        print "    success"
        return


    def migrateRecords(self):
        records = self.clerk.db.fetchall(self.oldtable)
        T = self.table
        
        from pyre.db.Column import Column
        attrs = filter(lambda a: isinstance(getattr(T, a), Column), T.__dict__.iterkeys())

        newrecords = []
        for r in records:
            t = T()
            for attr in attrs:
                try: value = getattr(r, attr)
                except AttributeError: continue
                setattr(t, attr, value)
                continue
            newrecords.append(t)
            continue
        
        return newrecords


    def dropTable(self, table):
        db = self.clerk.db
        print " -- dropping table %r" % table.name
        db.dropTable(table)
        print "    success"
        return


    def __init__(self, name='migratetable'):
        base.__init__(self, name)
        return


    def _configure(self):
        base._configure(self)
        self.table = self.inventory.table
        import os
        self.oldtablepath, self.oldtablename = os.path.split(self.inventory.oldtableurl)

        self.idd = self.inventory.idd
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        base._init(self)

        # initialize table registry
        import vnf.dom
        vnf.dom.register_alltables()

        # set id generator for referenceset
        def _id():
            from vnf.components.misc import new_id
            return new_id(self)
        vnf.dom.set_idgenerator(_id)
        self._import_old_table()
        return


    def _import_old_table(self):
        # read code
        import os
        codepath = os.path.expanduser(self.oldtablepath)
        code = open(codepath).read()

        import sys
        codedir = os.path.dirname(codepath)
        sys.path = [codedir] + sys.path
        d = {}; exec code in d
        self.oldtable = d[self.oldtablename]
        sys.path = sys.path[1:]
        
        self.table = self.clerk._getTable(self.table)
        return


    def _getPrivateDepositoryLocations(self):
        return ['../content', '../config']
    

# version
__id__ = "$Id$"

# End of file 
