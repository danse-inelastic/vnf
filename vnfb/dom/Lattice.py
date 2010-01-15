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


# data object
from matter.orm.Lattice import Lattice


# db table
from _ import o2t
LatticeTable = o2t(Lattice)


# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.mold.sequence = ['a', 'b', 'c', 'alpha', 'beta', 'gamma'] # 'base']
Lattice.customizeLubanObjectDrawer = customizeLubanObjectDrawer



# version
__id__ = "$Id$"

# End of file 
