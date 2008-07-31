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


from OwnedObject import OwnedObject
class VirtualObject(OwnedObject):

    import pyre.db
    
    type = pyre.db.varchar( name = 'type', length = 128 )
    type.meta['tip'] = 'type of the real object'
    
    reference = pyre.db.varchar(name='reference', length = 128 )
    reference.meta['tip'] = 'reference id in the table of the given type'

    pass # end of VirtualObject


# version
__id__ = "$Id$"

# End of file 
