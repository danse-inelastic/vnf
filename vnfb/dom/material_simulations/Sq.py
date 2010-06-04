# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from vsat.Sq import Sq
from vnfb.dom.AtomicStructure import StructureTable

# db table
from ComputationResult import ComputationResult
from _ import o2t
SqTable = o2t(Sq, {'subclassFrom': ComputationResult})
import dsaw.db
SqTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable)#, backref='')
    )

#SqTable.datafiles = [
#    'data.plot'
#    ]



# version
__id__ = "$Id$"

# End of file 
