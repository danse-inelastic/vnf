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



from registry import tableRegistry


# a handler to handle database requests about a referenceset for
# a particular container
class referenceset:


    def __init__(self, name, id, table):
        '''
        table, id: identify the parent record
        '''
        self.name = name
        self.table = table
        self.id = id
        return


    def dereference(self, db):
        records = self._get_referencetable_records( db )
        ret = []
        for record in records:
            key = record.elementlabel
            value = record.element.dereference( db )
            ret.append( (key, value) )
            continue
        return ret



    def clear(self, db):
        records = self._get_referencetable_records( db )
        for record in records:
            db.deleteRow( _ReferenceTable, where = "id='%s'" % record.id )
            continue
        return


    def delete(self, record, db):
        # here, the record is a db record that this reference set
        # refers to.
        # The record itself is not removed. it should be manually removed if necessary.
        temp = _ReferenceTable()
        temp.container = self._container_ref()
        temp.element = self._element_ref( record )
        where = "containerlabel='%s' and container='%s' and element='%s'" % (
            self.name, temp.container, temp.element)
        db.deleteRow( _ReferenceTable, where = where)
        return
    

    def add(self, record, db, name = ''):
        container_ref = self._container_ref()
        element_ref = self._element_ref( record )
        row = _ReferenceTable()
        row.id = self._id()
        row.containerlabel = self.name
        row.container = container_ref
        row.element = element_ref
        row.elementlabel = name
        db.insertRow( row )
        return


    def _container_ref(self):
        return self.table, self.id
    
    
    def _element_ref(self, record):
        return record.__class__, record.id


    def _id(self):
        from idgenerator import generator 
        if generator is None:
            msg = "id generator has not been set. please use vnf.dom.set_idgenerator to set id generator"
            raise RuntimeError, msg
        return generator()
    

    def _get_referencetable_records(self, db):
        container_ref = self._container_ref()
        temp = _ReferenceTable()
        temp.container = container_ref
        
        containerlabel = self.name
        where = "containerlabel='%s' and container='%s'" % (
            containerlabel, temp.container ) 
        return db.fetchall( _ReferenceTable, where = where )




# The table that stores referenceset
from Table import Table
class _ReferenceTable(Table):

    name = "_____referenceset_____"

    import pyre.db
    
    # columns
    id = pyre.db.varchar( name = 'id', length = 100 )
    id.constraints = 'PRIMARY KEY'

    containerlabel = pyre.db.varchar( name = 'containerlabel', length = 100 )
    elementlabel = pyre.db.varchar( name = "elementlabel", length = 100 )

    container = pyre.db.versatileReference( name = 'container', tableRegistry = tableRegistry )
    element = pyre.db.versatileReference( name = 'element', tableRegistry = tableRegistry )




# version
__id__ = "$Id$"

# End of file 
