# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import PhononDispersion, AbstractScatteringKernel as base
class PolyXtalCoherentPhononScatteringKernel(base):

    dispersion = None
    Ei = 70.
    max_energy_transfer = 55.
    max_momentum_transfer = 12.5


    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['dispersion', 'properties']
        drawer.mold.sequence = ['Ei', 'max_energy_transfer', 'max_momentum_transfer']


    pass # end of PolyXtalCoherentPhononScatteringKernel



from _ import AbstractScatteringKernelInventory as InvBase
class Inventory(InvBase):
    
    dispersion = InvBase.d.reference(
        name='dispersion', targettype=PhononDispersion, owned=0)

    Ei = InvBase.d.float(name = 'Ei', default = 70)
    
    max_energy_transfer = InvBase.d.float(name = 'max_energy_transfer', default = 55.)

    max_momentum_transfer = InvBase.d.float(name = 'max_momentum_transfer', default = 12.5)

    dbtablename = 'polyxtalcoherentphononscatteringkernels'

    pass # end of Inventory


PolyXtalCoherentPhononScatteringKernel.Inventory = Inventory
del Inventory
from _ import o2t, KernelTableBase
PolyXtalCoherentPhononScatteringKernelTable = o2t(
    PolyXtalCoherentPhononScatteringKernel,
    {'subclassFrom': KernelTableBase},
    )


# obsolete
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
