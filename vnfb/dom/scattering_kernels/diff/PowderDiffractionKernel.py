# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

#XXX: Finish?

from AbstractScatteringKernel import AbstractScatteringKernel as base, TableBase

class PowderDiffractionKernel(base):

    # scattering_length = 1.0

    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        # drawer.mold.sequence = ['scattering_length']
        return

    pass



InvBase = base.Inventory
class Inventory(InvBase):

    # scattering_length = InvBase.d.float(name = 'scattering_length', default = 1.)

    dbtablename = 'powderdiffractionkernels'

    pass


PowderDiffractionKernel.Inventory = Inventory
del Inventory


from _ import o2t
PowderDiffractionKernelTable = o2t(PowderDiffractionKernel, {'subclassFrom': TableBase},)

__date__ = "$Mar 8, 2011 9:27:32 PM$"


