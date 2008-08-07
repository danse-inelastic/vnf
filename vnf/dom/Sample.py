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


from registry import tableRegistry


from Table import Table
class Sample(Table):

    name = 'sample'

    import pyre.db

    id = pyre.db.varchar( name = 'id', length = 100)
    id.meta['tip'] = 'sample id'
    
    matter = pyre.db.versatileReference( name = 'matter', tableRegistry = tableRegistry)
    shape = pyre.db.versatileReference( name = 'shape', tableRegistry = tableRegistry)
    

# version
__id__ = "$Id$"

# End of file 
