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


from Atom import Atom
from Lattice import Lattice
from matter.orm.Structure import Structure


# db table
from _ import o2t
StructureTable = o2t(Structure)

# more cols
import dsaw.db
StructureTable.addColumn(dsaw.db.date(name='date'))

# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['lattice', 'atoms', 'properties',]
    drawer.readonly_view_sequence =  ['lattice', 'atoms', 'primitive_unitcell', 'properties',]
    drawer.mold.sequence = ['short_description', 'spacegroupno']
Structure.customizeLubanObjectDrawer = customizeLubanObjectDrawer


# version
__id__ = "$Id$"

# End of file 
