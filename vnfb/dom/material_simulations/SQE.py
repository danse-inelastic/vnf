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

from vsat.SQE import SQE
from vnfb.dom.AtomicStructure import StructureTable

# db table
from ComputationResult import ComputationResult
from _ import o2t
SQETable = o2t(SQE, {'subclassFrom': ComputationResult})
import dsaw.db
SQETable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable, backref='sqes')
    )


SQETable.histogramh5 = 'data.h5'
SQETable.ncfile = 'data.nc'
SQETable.datafiles = [
    SQETable.histogramh5,
    SQETable.ncfile,
    ]



# version
__id__ = "$Id$"

# End of file 
