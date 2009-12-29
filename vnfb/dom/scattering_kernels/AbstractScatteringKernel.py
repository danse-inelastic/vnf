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


# base class for all scattering kernel objects
class AbstractScatteringKernel(object):

    matter = None
    
    pass


# base class for all scattering kernel orm Inventory
from dsaw.model.Inventory import Inventory as InvBase
from _ import AtomicStructure
class AbstractScatteringKernelInventory(InvBase):

    matter = InvBase.d.reference(name='matter', targettype=None, targettypes=[AtomicStructure])
    


# version
__id__ = "$Id$"

# End of file 
