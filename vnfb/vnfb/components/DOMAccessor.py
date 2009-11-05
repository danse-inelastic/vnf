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


class DOMAccessor( base ):

    db = None

    def __init__(self, name, facility = 'dom-accessor'):
        super(DOMAccessor, self).__init__(name, facility)
        return
    

    # generic accessing methods
    def updateRecordWithID(self, record):
        'update a record. assumes that it has a "id" column'
        return self.db.updateRecord(record)


    def getRecordByID(self, tablename, id):
        from dsaw.db.Table import Table as TableBase
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


    def _getUsername(self):
        return self.director.sentry.username


    def _getTable(self, name):
        return self.db.getTable(name)


    def _getRecordByID(self, table, id ):
        all = self.db.fetchall( table, where = "id='%s'" % id )
        if len(all) == 1:
            return all[0]
        raise RuntimeError, "Cannot find record of id=%s in table %s" % (
            id, table.__name__)
        

# version
__id__ = "$Id$"

# End of file 
