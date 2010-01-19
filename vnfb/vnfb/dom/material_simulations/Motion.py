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
from vsat.Motion import Motion as MotionDO
from vnfb.dom.AtomicStructure import StructureTable

# orm

# "Holder" in vnf
from ComputationResult import ComputationResult
Motion = o2t(MotionDO, {'subclassFrom': ComputationResult})

import dsaw.db
Motion.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable, backref='motion')
    )

#PhononDOSTable.datafiles = [
#    'data.idf',
#    ]



# version
__id__ = "$Id$"

# End of file 
