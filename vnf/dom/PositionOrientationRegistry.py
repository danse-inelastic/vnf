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


from Table import Table


class PositionOrientationRegistry(Table):

    '''Each record in this registry describes the position
    and the orientation of an element in a container.

    When reference_id is '', the reference is the container.

    When reference_id is not empty, the reference is another
    element of the container.
    '''

    import pyre.db
    
    # columns
    id = pyre.db.varchar( name = 'id', length = 100 )
    id.constraints = 'PRIMARY KEY'
    
    container_id = pyre.db.varchar( name = 'container_id', length = 100)
    
    element_label = pyre.db.varchar( name = 'element_label', length = 100 )
    
    position = pyre.db.doubleArray(
        name = 'position',  default = [0.,0.,0.] )
    orientation = pyre.db.doubleArray(
        name = 'orientation', default = [0.,0.,0.] )
    
    reference_label = pyre.db.varchar(
        name = 'reference_label', length = 100, default = '')
    
    pass # end of PositionOrientationRegistry


# version
__id__ = "$Id$"

# End of file 
