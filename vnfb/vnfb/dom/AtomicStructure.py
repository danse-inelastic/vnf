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


from matter.Atom import Atom
Atom.Inventory.dbtablename = 'atoms'
AtomTable = o2t(Atom)
def customizeLubanObjectDrawer(self, drawer):
    drawer.mold.sequence = ['element', 'xyz', 'label', 'occupancy',]
Atom.customizeLubanObjectDrawer = customizeLubanObjectDrawer


from matter.Lattice import Lattice
Lattice.Inventory.dbtablename = 'lattices'
LatticeTable = o2t(Lattice)

def customizeLubanObjectDrawer(self, drawer):
    drawer.mold.sequence = ['a', 'b', 'c', 'alpha', 'beta', 'gamma']
Lattice.customizeLubanObjectDrawer = customizeLubanObjectDrawer


from matter.Structure import Structure
Structure.Inventory.dbtablename = 'atomicstructures'
StructureTable = o2t(Structure)

def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['lattice', 'atoms', 'properties']
    drawer.mold.sequence = ['short_description', 'spacegroupno']
Structure.customizeLubanObjectDrawer = customizeLubanObjectDrawer

# version
__id__ = "$Id$"

# End of file 
