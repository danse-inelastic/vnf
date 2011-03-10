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

#XXX: Finish!!!

from _ import AbstractScatteringKernel as base, TableBase

class PowderDiffractionKernel(base):

    dfraction   = 1e-5    # Dd_over_d
    dwfactor    = 1.      # DebyeWaller_factor

    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = [
            'dfraction',
            'dwfactor'
            ]
        return


InvBase = base.Inventory
class Inventory(InvBase):

    dfraction   = InvBase.d.float(name = 'dfraction', default = 1e-5)
    dwfactor    = InvBase.d.float(name = 'dwfactor', default = 1.)

    dbtablename = 'powderdiffractionkernels'

    pass


PowderDiffractionKernel.Inventory = Inventory
del Inventory

from _ import o2t
PowderDiffractionKernelTable = o2t(PowderDiffractionKernel, {'subclassFrom': TableBase},)

__date__ = "$Mar 8, 2011 9:27:32 PM$"


