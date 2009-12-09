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
from Atom import Atom
from Lattice import Lattice
from matter.Structure import Structure


# dsaw.model helpers
def __establishInventory__(self, inventory):
    inventory.short_description = self.description
    inventory.lattice = self.lattice
    inventory.spacegroupno = self.sg.number
    inventory.chemical_formula = self.getChemicalFormula()
    inventory.atoms = self # the implementation of Structure class is that structure is inherited from list, and the items are atoms.
    return
Structure.__establishInventory__ = __establishInventory__

def __restoreFromInventory__(self, inventory):
    self.__init__(atoms=inventory.atoms,
                  lattice=inventory.lattice,
                  sgid=inventory.spacegroupno,
                  description=inventory.short_description,
                  )
Structure.__restoreFromInventory__ = __restoreFromInventory__


# inventory
from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    short_description = InvBase.d.str(
        name = 'short_description', max_length = 256, default ="", label='Description')
    lattice = InvBase.d.reference(name = 'lattice', targettype=Lattice, owned=1)
    atoms = InvBase.d.referenceSet(name='atoms', targettype=Atom, owned=1)
    spacegroupno = InvBase.d.int(name = 'spacegroupno', default =1, label='Spacegroup #')
    chemical_formula = InvBase.d.str(name='chemical_formula', max_length=1024)

    dbtablename = 'atomicstructures'

Structure.Inventory = Inventory


# db table
StructureTable = o2t(Structure)

# more cols
import dsaw.db
StructureTable.addColumn(dsaw.db.date(name='date'))

# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['lattice', 'atoms', 'properties']
    drawer.mold.sequence = ['short_description', 'spacegroupno']
Structure.customizeLubanObjectDrawer = customizeLubanObjectDrawer


# version
__id__ = "$Id$"

# End of file 
