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


from PhononDispersion import PhononDispersion

from registry import tableRegistry

from ScatteringKernel import ScatteringKernel as base
class PolyXtalCoherentPhononScatteringKernel(base):

    name = 'polyxtalcoherentphononscatteringkernels'
    
    import dsaw.db

    dispersion = dsaw.db.reference(name = 'dispersion', table = PhononDispersion)

    Ei = dsaw.db.real(name = 'Ei', default = 70)
    
    max_energy_transfer = dsaw.db.real(name = 'max_energy_transfer', default = 55.)

    max_momentum_transfer = dsaw.db.real(name = 'max_momentum_transfer', default = 12.5)

    pass # end of PolyXtalCoherentPhononScatteringKernel


def inittable(db):
    def k(id, dispersion, Ei, max_energy_transfer, max_momentum_transfer):
        r = PolyXtalCoherentPhononScatteringKernel()
        r.id = id
        r.Ei = Ei
        r.dispersion = dispersion
        r.max_energy_transfer = max_energy_transfer
        r.max_momentum_transfer = max_momentum_transfer
        return r

    from PhononDispersion import PhononDispersion
    records = [
        k('polyxtalcoherentphononscatteringkernel-fccNi-0',
          'phonon-dispersion-fccNi-0',
          70.,
          55.,
          12.5,
          ),
        ]

    for r in records: db.insertRow(r)
    return


def initids():
    return [
        'polyxtalcoherentphononscatteringkernel-fccNi-0',
        ]


# version
__id__ = "$Id$"

# End of file 
