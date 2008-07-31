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
class DetectorSystem_fromXML(OwnedObject):

    name = 'detectorsystem_fromxmls'

    import pyre.db

    tofmin = pyre.db.real( name = 'tofmin', default = 3000. )
    tofmin.meta['tip'] = 'minimum tof. unit: microsecond'
    
    tofmax = pyre.db.real( name = 'tofmax', default = 6000. )
    tofmax.meta['tip'] = 'maximum tof. unit: microsecond'

    ntofbins = pyre.db.integer( name = 'ntofbins', default = 300 )
    ntofbins.meta['tip'] = 'number of tof bins'

    pass # end of DetectorSystem_fromXML


# version
__id__ = "$Id$"

# End of file 
