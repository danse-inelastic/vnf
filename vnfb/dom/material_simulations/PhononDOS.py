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


from vsat.PhononDOS import PhononDOS

from vnf.dom.AtomicStructure import StructureTable
# db table
from ComputationResult import ComputationResult
PhononDOSTable = o2t(PhononDOS, {'subclassFrom': ComputationResult})
import dsaw.db
PhononDOSTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable, backref='phonondoses')
    )

PhononDOSTable.datafiles = ['data.idf']



# version
__id__ = "$Id$"

# End of file 
