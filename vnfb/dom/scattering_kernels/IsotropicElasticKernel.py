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


# kernel that scatters neutron isotropicall and elastically


from AbstractScatteringKernel import AbstractScatteringKernel as base, TableBase

class IsotropicElasticKernel(base):

    # scattering_length = 1.0

    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        # drawer.mold.sequence = ['scattering_length']
        return
    
    pass 



InvBase = base.Inventory
class Inventory(InvBase):

    # scattering_length = InvBase.d.float(name = 'scattering_length', default = 1.)
    
    dbtablename = 'isotropicelastickernels'
    
    pass 


IsotropicElasticKernel.Inventory = Inventory
del Inventory


from _ import o2t
IsotropicElasticKernelTable = o2t(
    IsotropicElasticKernel,
    {'subclassFrom': TableBase},
    )


# version
__id__ = "$Id$"

# End of file 
