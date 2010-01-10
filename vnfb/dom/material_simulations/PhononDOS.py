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

from _ import o2t


# data object
class PhononDOS:

    matter = None

# orm
from vnfb.dom.AtomicStructure import Structure, StructureTable

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name='matter', targettype=Structure, owned=0)

    dbtablename = 'phonondoses'

PhononDOS.Inventory = Inventory


# db table
from ComputationResult import ComputationResult
PhononDOSTable = o2t(PhononDOS, {'subclassFrom': ComputationResult})
import dsaw.db
PhononDOSTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable, backref='phonondoses')
    )

PhononDOSTable.datafiles = [
    'data.idf',
    ]



# version
__id__ = "$Id$"

# End of file 
