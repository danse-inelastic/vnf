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


from NeutronComponent import NeutronComponent as base
class MonochromaticSource(base):

    name = 'monochromaticsources'

    import pyre.db

    energy = pyre.db.real( name = 'energy', default = 70. )
    energy.meta['tip'] = 'neutron energy. unit: meV'
    
    pass # end of MonochromaticSource


# version
__id__ = "$Id$"

# End of file 
