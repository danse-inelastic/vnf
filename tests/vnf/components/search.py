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


# table registry for reference
from vnf.dom.registry import tableRegistry

# tables for testing references
from vnf.dom.Table import Table
class Table1(Table):
    name = '__test_references_to_be_referred__'
    import pyre.db
    id = pyre.db.varchar(name='id', length=64)
    id.constraints = 'PRIMARY KEY'
    
class Table2(Table):
    name = '__test_references__'

    import pyre.db
    id = pyre.db.varchar(name='id', length=64)
    id.constraints = 'PRIMARY KEY'

    ref1 = pyre.db.reference(name='ref1', table=Table1)
    ref2 = pyre.db.versatileReference(name='ref2', tableRegistry=tableRegistry, length=128)

    import vnf.dom
    refset1 = vnf.dom.referenceSet(name='refset1')

tables = [
    Table1,
    Table2,
    ]
from vnf.dom._hidden_tables import tables as hiddentables
hiddentables = hiddentables()
alltables = tables + hiddentables
for T in alltables: tableRegistry.register(T)



import random
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
def gid():
    return ''.join(random.sample(alphabet, 6))


class App(Script):


    class Inventory(Script.Inventory):

        import pyre.inventory
        import vnf.components
        clerk = pyre.inventory.facility('clerk', factory=vnf.components.clerk)
        
    def _init(self, *args, **kwds):
        self.clerk = 'test'


    def main(self, *args, **kwds):
        clerk = self.clerk
        # for some reason my _configure method doesn't work.  so i have to
        # do it manually here
        #clerk.db = clerk.inventory.db
        #clerk.db = 'test'
        #clerk.inventory.db = 'test'
        self._createTables()

        self._testSearch()
#
#        self._testRemoveReferredRecord()
#        self._testRemoveVersatileReferredRecord()
#        self._testRemoveRecordInRefset()
        return
    
    def _testSearch(self):
        pass


    def _testRemoveReferredRecord(self):
        clerk = self.clerk

        # create some records
        t1 = Table1()
        t1.id = 'testid001'
        clerk.newRecord(t1)

        # t2 refer to t1 thru ref1
        t2 = Table2()
        t2.id = 'testid002'
        t2.ref1 = t1
        clerk.newRecord(t2)

        #get the referred record
        record = self.getRecordByID(Table1, 'testid001')

        #try to delete the referred record
        clerk.deleteRecord(record)

        #make sure the delete does not really happen
        record1 = self.getRecordByID(Table1, 'testid001')
        assert record1 is not None

        #clean up
        clerk.deleteRecord(t2)
        clerk.deleteRecord(t1)
        assert self.getRecordByID(Table1, 'testid001') is None
        assert self.getRecordByID(Table2, 'testid002') is None
        return


    def _testRemoveVersatileReferredRecord(self):
        clerk = self.clerk

        # create some records
        t1 = Table1()
        t1.id = 'testid001'
        clerk.newRecord(t1)

        # t2 refer to t1 thru ref2
        t2 = Table2()
        t2.id = 'testid002'
        t2.ref2 = t1
        clerk.newRecord(t2)

        #get the referred record
        record = self.getRecordByID(Table1, 'testid001')

        #try to delete the referred record
        clerk.deleteRecord(record)

        #make sure the delete does not really happen
        record1 = self.getRecordByID(Table1, 'testid001')
        assert record1 is not None

        #clean up
        clerk.deleteRecord(t2)
        clerk.deleteRecord(t1)
        assert self.getRecordByID(Table1, 'testid001') is None
        assert self.getRecordByID(Table2, 'testid002') is None
        return


    def _testRemoveRecordInRefset(self):
        clerk = self.clerk

        # create some records
        t1 = Table1()
        t1.id = 'testid001'
        clerk.newRecord(t1)

        # t2 refer to t1 thru refset1
        t2 = Table2()
        t2.id = 'testid002'
        clerk.newRecord(t2)
        t2.refset1.add(t1, self.clerk.db)

        #get the referred record
        record = self.getRecordByID(Table1, 'testid001')
        assert record is not None

        #try to delete the referred record
        clerk.deleteRecord(record)

        #make sure the delete does not really happen
        record1 = self.getRecordByID(Table1, 'testid001')
        assert record1 is not None

        #clean up
        assert not clerk._referred(t2)
        clerk.deleteRecord(t2)
        assert not clerk._referred(t1)
        clerk.deleteRecord(t1)
        assert self.getRecordByID(Table1, 'testid001') is None
        assert self.getRecordByID(Table2, 'testid002') is None
        return


    def getRecordByID(self, table, id):
        clerk = self.clerk
        try:
            r = clerk._getRecordByID(table, id)
            return r
        except RuntimeError:
            import traceback
            e = traceback.format_exc()
            self._debug.log(e)
            return


    def _createTables(self):
        for table in tables:
            #self._dropTable(table)
            self._createTable(table)
        return


    def _createTable(self, table):
        db = self.clerk.db
        
        print " -- creating table %r" % table.name
        try:
            db.createTable(table)
        except db.ProgrammingError, msg:
            print "    failed; table exists?"
            print msg
        else:
            print "    success"
        return            


    def _dropTable(self, table):
        db = self.clerk.db
        
        print " -- dropping table %r" % table.name
        try:
            db.dropTable(table)
        except db.ProgrammingError:
            print "    failed; table doesn't exist?"
        else:
            print "    success"

        return


    def __init__(self):
        Script.__init__(self, 'test-clerk')
        return


    def _defaults(self):
        Script._defaults(self)
        clerk = self.inventory.clerk
        clerk.inventory.db = 'vnf'
        clerk.inventory.dbwrapper = 'psycopg2'
        return


    def _configure(self):
        Script._configure(self)
        self.clerk = self.inventory.clerk
        self.clerk.director = self
        return


    def _init(self):
        Script._init(self)
        import vnf.dom
        vnf.dom.set_idgenerator(gid)
        return


def main():
    app = App()
    return app.run()


# main
if __name__ == '__main__':
    import journal
    journal.info('clerk').activate()
    journal.debug('clerk').activate()
    #journal.debug('reference-manager').activate()
    #journal.debug('test-clerk').activate()
    # invoke the application shell
    main()


# version
__id__ = "$Id$"

# End of file 
