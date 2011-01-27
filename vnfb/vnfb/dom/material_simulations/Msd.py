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

from vsat.Msd import Msd
from vnfb.dom.AtomicStructure import StructureTable

# db table
from ComputationResult import ComputationResult
from _ import o2t
MsdTable = o2t(Msd, {'subclassFrom': ComputationResult})
import dsaw.db
MsdTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable)#, backref='')
    )

#EisfTable.datafiles = [
#    'data.plot'
#    ]



# version
__id__ = "$Id$"

# End of file 
