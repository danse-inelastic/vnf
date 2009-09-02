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


from OwnedObject import OwnedObject as base
class Sample(base):

    name = 'samples'

    import dsaw.db
    
    matter = dsaw.db.versatileReference( name = 'matter', tableRegistry = tableRegistry)
    shape = dsaw.db.versatileReference( name = 'shape', tableRegistry = tableRegistry)
    

# version
__id__ = "$Id$"

# End of file 
