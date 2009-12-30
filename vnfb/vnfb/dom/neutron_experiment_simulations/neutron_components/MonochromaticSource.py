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


from AbstractNeutronComponent import AbstractNeutronComponent as base
class MonochromaticSource(base):

    name = 'monochromaticsources'

    import dsaw.db

    energy = dsaw.db.real( name = 'energy', default = 70. )
    energy.meta['tip'] = 'neutron energy. unit: meV'
    
    pass # end of MonochromaticSource


# version
__id__ = "$Id$"

# End of file 
