# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from Atom import Atom
from Lattice import Lattice
from matter.orm.Structure import Structure

# db table
from _ import o2t, AbstractOwnedObjectBase
StructureTable = o2t(Structure, {'subclassFrom': AbstractOwnedObjectBase})


# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['lattice', 'atoms', 'properties',]
    drawer.readonly_view_sequence =  ['lattice', 'atoms', 
                                      'primitive_unitcell', 'properties',]
    drawer.mold.sequence = ['short_description', 'spacegroupno']
Structure.customizeLubanObjectDrawer = customizeLubanObjectDrawer

Structure.luban_orm_actor = "orm/atomicstructures"

# version
__id__ = "$Id$"

# End of file 
