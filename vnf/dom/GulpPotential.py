# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



from OwnedObject import OwnedObject as base
class GulpPotential(base):

    name = 'gulppotential'

    path = '../content/data/gulppotentials'

    import pyre
    potential_name = pyre.db.varchar(name='potential_name', length=2048, default='potential')
    
    elements = pyre.db.varcharArray(name = 'elements', length = 2, default = [] )
    elements.meta['tip'] = 'elements within the potential'

# version
__id__ = "$Id$"

# End of file 
