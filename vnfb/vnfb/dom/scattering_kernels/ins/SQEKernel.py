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


from _ import PhononDispersion, AbstractScatteringKernel as base

class SQEKernel(base):

    sqe = None

    Qmin = 0.
    Qmax = 10.

    Emin = -50.
    Emax = 50.
    
    pass # end of SQEKernel



from _ import AbstractScatteringKernelInventory as InvBase, sqe_types
class Inventory(InvBase):

    sqe = InvBase.d.reference(
        name = 'sqe',
        targettype=None, targettypes=[sqe_types],
        owned = 0,
        )

    Qmin = InvBase.d.float(name = 'Qmin', default = 0)
    Qmax = InvBase.d.float(name = 'Qmax', default = 10)

    Emin = InvBase.d.float(name = 'Emin', default = -50)
    Emax = InvBase.d.float(name = 'Emax', default = 50)
    
    dbtablename = 'sqekernels'
    
    pass # end of Inventory


SQEKernel.Inventory = Inventory
del Inventory
from _ import o2t, AbstractOwnedObjectBase
SQEKernelTable = o2t(
    SQEKernel,
    {'subclassFrom': AbstractOwnedObjectBase},
    )


# version
__id__ = "$Id$"

# End of file 
