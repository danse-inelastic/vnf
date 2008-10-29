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
        name = 'dispersion', tableRegistry = tableRegistry )
    
    max_energy_transfer = pyre.db.real( name = 'max_energy_transfer', default = 55. )

    max_momentum_transfer = pyre.db.real( name = 'max_momentum_transfer', default = 12.5 )

    pass # end of PolyXtalCoherentPhononScatteringKernel


def inittable(db):
    def k( id, dispersion, max_energy_transfer, max_momentum_transfer):
        r = PolyXtalCoherentPhononScatteringKernel()
        r.id = id
        r.dispersion = dispersion
        r.max_energy_transfer = max_energy_transfer
        r.max_momentum_transfer = max_momentum_transfer
        return r

    from IDFPhononDispersion import IDFPhononDispersion
    records = [
        k( 'polyxtalcoherentphononscatteringkernel-fccNi-0',
           (IDFPhononDispersion, 'idf-phonon-dispersion-fccNi-0'),
           55.,
           12.5,
           ),
        ]

    for r in records: db.insertRow( r )
    return


# version
__id__ = "$Id$"

# End of file 
