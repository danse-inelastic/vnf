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

from vsat.Eisf import Eisf
from vnfb.dom.AtomicStructure import StructureTable

# db table
from ComputationResult import ComputationResult
from _ import o2t
EisfTable = o2t(Eisf, {'subclassFrom': ComputationResult})
import dsaw.db
EisfTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable)#, backref='')
    )

#EisfTable.datafiles = [
#    'data.plot'
#    ]



# version
__id__ = "$Id$"

# End of file 
