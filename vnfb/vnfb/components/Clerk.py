# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from pyre.components.Component import Component as base


class Clerk( base ):

    class Inventory( base.Inventory):

        import pyre.inventory
        db = pyre.inventory.str('db', default = 'vnf' )
        dbwrapper = pyre.inventory.str('dbwrapper', default = 'psycopg2')
        

    def __init__(self, name = 'clerk', facility = 'clerk'):
        base.__init__(self, name, facility)
        return
    

    # user table
    def indexUsers(self, where=None):
        """create an index of all users that meet the specified criteria"""
        from vnf.dom.User import User
        index = {}
        users = self.db.fetchall(User, where=where)
        for user in users:
            index[user.username] = user
            continue
        return index


    def indexActiveUsers(self):
        return self.indexUsers()


    def getUser(self, username):
        from gongshuzi.dom.User import User
        users = self.db.fetchall(User, where="username='%s'" % username)
        if not users: raise RuntimeError, "user %r not found" % username
        assert len(users) == 1
        return users[0]


    def getUserInfo(self, username):
        from gongshuzi.dom.Registrant import Registrant
        registrants = self.db.fetchall(Registrant, where="username='%s'"% username)
        if not registrants: raise RuntimeError, "user %r not found" % username
        assert len(registrants) == 1
        return registrants[0]
        

    # generic accessing methods
    def updateRecordWithID(self, record):
        'update a record. assumes that it has a "id" column'
        id = record.id
        where = "id='%s'" % id
        
        assignments = []
        
        # get the column names and couple them with the new values
        for column, descriptor in record._columnRegistry.iteritems():
            value = descriptor.getFormattedValue(record)
            assignments.append( (column, value) )
            continue

        # update the row, or in other words, record
        self.db.updateRow(record.__class__, assignments, where)
        
        return record


    def getRecordByID(self, tablename, id):
        from pyre.db.Table import Table as TableBase
        if isinstance(tablename, basestring):
            Table = self._getTable(tablename)
        elif issubclass(tablename, TableBase):
            Table = tablename
        else:
            raise ValueError, 'tablename must be a string or a table class: %s' % tablename
        return self._getRecordByID(Table, id)
    
    
    def insertNewOwnedRecord(self, table, owner = None):
        '''create a new record for the given table.

        The given table is assumed to have following fields:
          - id
          - creator
          - date
        '''
        if isinstance(table, str): table = self._getTable(table)
        
        director = self.director
        id = director.getGUID()

        record = table()
        record.id = id

        if not owner: 
            owner = director.sentry.username
        record.creator = owner
        
        self.insertNewRecord( record )
        return record


    def insertNewRecordWithID(self, table):
        '''create a new record for the given table and store it in the db.

        The given table is assumed to have following fields:
          - id
        '''
        record = self.createRecordWithID(table)
        return self.insertNewRecord(record)
    
    
    def createRecordWithID(self, table):
        '''create a new record for the given table but do not store it in the db.

        The given table is assumed to have following fields:
          - id
        '''
        record = table()
        
        director = self.director
        id = director.getGUID()
        record.id = id

        return record


    def insertNewRecord(self, record):
        'insert a new record into db'
        try:
            self.db.insertRow( record )
        except:
            columns = record.getColumnNames()
            values = [ record.getColumnValue( column ) for column in columns ]
            s = ','.join(
                [ '%s=%s' % (column, value)
                  for column, value in zip(columns, values)
                  ] )
            self._debug.log( 'failed to insert record: %s' % s)
            raise
        return record


    def deleteRecordWithID(self, record):
        'delete a record. assumes that it has a "id" column'
        self.db.deleteRow(record.__class__, where="id='%s'" % record.id)
        return
    

    def dereference(self, pointer):
        '''dereference a "pointer"'''
        return pointer.dereference(self.db)


    def _getTable(self, name):
        return self.db.getTable(name)


    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)
        

    def _configure(self):
        base._configure(self)
        self.db = self.inventory.db
        self.dbwrapper = self.inventory.dbwrapper
        return


    def _init(self):
        base._init(self)

        from dsaw.db import connect
        self.db = connect(self.db, self.dbwrapper)
        self.db.autocommit()

        # create system tables if necessary
##         system_tables = self.db._systemtables
##         for table in system_tables.itertables():
##             try:
##                 self.db.createTable(table)
##             except:
##                 import traceback
##                 traceback.print_exc()
##             continue

        # register tables
        from vnf.dom import alltables
        for table in alltables():
            self.db.registerTable(table)
        return


    def _fini(self):
        base._fini(self)
        return
    


# version
__id__ = "$Id$"

# End of file 
