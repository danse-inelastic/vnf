#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


idgenerator = None  # unique id generator

class referenceset:

    separator = '###'

    def __init__(self, name, id, table, tableRegistry):
        '''
        name: name of this reference set
        table, id: identify the parent record
        '''
        self.name = name
        self.table = table
        self.id = id
        self.tableRegistry = tableRegistry
        return


    def key(self):
        tokens = [ self.name, self.table.name, self.id ]
        return self.separator.join( tokens )
    
    
    def dereference(self, db):
        records = self._get_referencetable_records( db )
        references = [ record.remotekey for record in records ]
        return [ self._dereference( r, db ) for r in references ]


    def clear(self, db):
        records = self._get_referencetable_records( db )
        for record in records:
            db.deleteRow( _ReferenceTable, where = 'id="%s"' % record.id )
            continue
        return


    def delete(self, record, db):
        # here, the record is a db record that this reference set
        # refers to.
        where = 'localkey="%s" and remotekey="%s"' % (
            self.key(), self._remotekey(record))
        db.deleteRow( _ReferenceTable, where = where)
        return
    

    def add(self, references, db):
        localkey = self.key()
        for reference in references:
            remotekey = self._remotekey( reference )
            row = _ReferenceTable()
            row.id = self._id()
            row.localkey = localkey
            row.remotekey = remotekey
            db.insertRow( row )
            continue
        return


    def _remotekey(self, record):
        tokens = [ record.__class__.name, record.id ]
        return self.separator.join( tokens )


    def _id(self):
        generator = idgenerator
        if generator is None:
            msg = "id generator has not been set. please use pyre.db.set_referencesettable_idgenerator to set id generator"
            raise RuntimeError, msg
        return generator()
    

    def _dereference(self, reference_str, db):
        table, id = self._decode_reference( reference_str )
        return _dereference( id, table, db )
    

    def _decode_reference(self, reference):
        tablename, id = reference.split( self.separator )
        table = self.tableRegistry.get( tablename )
        return table, id


    def _get_referencetable_records(self, db):
        localkey = self.key()
        return db.fetchall( _ReferenceTable, where = "localkey='%s'" % localkey )



def _dereference(id, table, db):
    return reference(id, table).dereference( db )
from pyre.db._reference import reference


from Table import Table
class _ReferenceTable(Table):

    name = "_____referenceset_____"

    import pyre.db
    
    # columns
    id = pyre.db.varchar( name = 'id', length = 100 )
    id.constraints = 'PRIMARY KEY'
    
    localkey = pyre.db.varchar( name = 'localkey', length = 100 )
    remotekey = pyre.db.varchar( name = 'remotekey', length = 100 )



# version
__id__ = "$Id$"

# End of file 
