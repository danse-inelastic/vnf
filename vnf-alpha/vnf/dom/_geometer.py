# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from registry import tableRegistry


class registry:

    separator = '###'

    def __init__(self, container_id, container_table):
        '''
        container_table, container_id: identify the container
        '''
        self.table = container_table
        self.id = container_id
        return


    def dereference(self, db):
        records = self._get_records( db )
        ret = {}
        for r in records:
            k = r.element_label
            v = r
            ret[k] = v
            continue
        return ret
        

    def delete(self, element, db):
        '''remove an elment from registry'''
        temp = PositionOrientationRegistry()
        temp.container = self._container_ref()
        where = "container='%s' and element_label='%s'" % (
            temp.container, element)
        db.deleteRow( PositionOrientationRegistry, where = where)
        return
    

    def register(self, element, position, orientation, db, reference = ''):
        temp = PositionOrientationRegistry()
        temp.container = self._container_ref()
        temp.element_label = element
        temp.position = position
        temp.orientation = orientation
        temp.reference_label = reference
        temp.id = self._id()
        db.insertRow( temp )        
        return


    def _container_ref(self):
        return self.table, self.id
    
    def _id(self):
        from idgenerator import generator
        if generator is None:
            msg = "id generator has not been set. please use dsaw.db.set_referencesettable_idgenerator to set id generator"
            raise RuntimeError, msg
        return generator()
    

    def _get_records(self, db):
        temp = PositionOrientationRegistry()
        temp.container = self._container_ref()
        where = "container='%s'" % temp.container
        return db.fetchall( PositionOrientationRegistry, where = where)



# The db table
from Table import Table

class PositionOrientationRegistry(Table):
    
    '''Each record in this registry describes the position
    and the orientation of an element in a container.

    Elements are identified by their labels; it is not necessary
    to explicitly specify (table, id). The reason is that the
    container should have an "elements" attribute that is a
    "referenceset" that explicitly identify the elements.

    When reference_label is '', the reference is the container.

    When reference_label is not empty, the reference is another
    element of the container.
    '''

    name = '__position_orientation_registry__'
    
    import dsaw.db
    
    # columns
    id = dsaw.db.varchar( name = 'id', length = 64 )
    id.constraints = 'PRIMARY KEY'
    
    container = dsaw.db.versatileReference(
        name = 'container', tableRegistry = tableRegistry)
    
    element_label = dsaw.db.varchar( name = 'element_label', length = 64 )
    
    position = dsaw.db.doubleArray(
        name = 'position',  default = [0.,0.,0.] )
    orientation = dsaw.db.doubleArray(
        name = 'orientation', default = [0.,0.,0.] )
    
    reference_label = dsaw.db.varchar(
        name = 'reference_label', length = 64, default = '')
    
    pass # end of PositionOrientationRegistry


# version
__id__ = "$Id$"

# End of file 
