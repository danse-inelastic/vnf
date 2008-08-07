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


from registry import tableRegistry

from ScatteringKernel import ScatteringKernel as base
class PolyXtalCoherentPhononScatteringKernel(base):

    name = 'polyxtalcoherentphononscatteringkernels'
    
    import pyre.db

    dispersion = pyre.db.versatileReference(
        name = 'dispersion_id', tableRegistry = tableRegistry )
    
    max_energy_transfer = pyre.db.real( name = 'max_energy_transfer', default = 55. )

    max_momentum_transfer = pyre.db.real( name = 'max_momentum_transfer', default = 12.5 )

    pass # end of PolyXtalCoherentPhononScatteringKernel


# version
__id__ = "$Id$"

# End of file 
