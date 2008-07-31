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
class PolyXtalCoherentPhononScatteringKernel(OwnedObject):

    name = 'polyxtalcoherentphononscatteringkernels'
    
    import pyre.db

    dispersion_id = pyre.db.varchar( name = 'dispersion_id', length = 100 )
    dispersion_id.meta['tip'] = 'reference id in the dispersion table'
    
    max_energy_transfer = pyre.db.real( name = 'max_energy_transfer', default = 55. )

    max_momentum_transfer = pyre.db.real( name = 'max_momentum_transfer', default = 12.5 )

    pass # end of PolyXtalCoherentPhononScatteringKernel


# version
__id__ = "$Id$"

# End of file 
