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


from matter.Lattice import Lattice
Lattice.Inventory.dbtablename = 'lattices'
LatticeTable = o2t(Lattice)


from matter.Structure import Structure
Structure.Inventory.dbtablename = 'atomicstructures'
StructureTable = o2t(Structure)


# version
__id__ = "$Id$"

# End of file 
