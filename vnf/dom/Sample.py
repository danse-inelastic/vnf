# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table
class Sample(Table):

    name = 'sample'

    import pyre.db

    id = pyre.db.varchar( name = 'id', length = 100)
    id.meta['tip'] = 'sample id'
    
    matter_id = pyre.db.varchar( name = 'matter_id', length = 100)
    matter_id.meta['tip'] = 'matter_id'
    
    shape_id = pyre.db.varchar( name = 'shape_id', length = 100)
    shape_id.meta['tip'] = 'shape_id'


# version
__id__ = "$Id$"

# End of file 
