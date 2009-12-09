# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import o2t
from dsaw.model.Inventory import Inventory as InvBase


# data object
from matter.Lattice import Lattice


# dsaw.model inventory
class Inventory(InvBase):

    a = InvBase.d.float(name = 'a', default=1.0, validator=InvBase.v.positive)
    b = InvBase.d.float(name = 'b', default=1.0, validator=InvBase.v.positive)
    c = InvBase.d.float(name = 'c', default=1.0, validator=InvBase.v.positive)
    alpha = InvBase.d.float(name = 'alpha', default=90.0, validator=InvBase.v.range(0,180,brackets='()'))
    beta = InvBase.d.float(name = 'beta', default=90.0, validator=InvBase.v.range(0,180,brackets='()'))
    gamma = InvBase.d.float(name = 'gamma', default=90.0, validator=InvBase.v.range(0,180,brackets='()'))

    dbtablename = 'lattices'
    
Lattice.Inventory = Inventory
del Inventory


# db table
LatticeTable = o2t(Lattice)


# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.mold.sequence = ['a', 'b', 'c', 'alpha', 'beta', 'gamma']
Lattice.customizeLubanObjectDrawer = customizeLubanObjectDrawer



# version
__id__ = "$Id$"

# End of file 
