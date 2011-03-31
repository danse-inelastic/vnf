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

from _ import o2t


# data object
from vsat.Trajectory import Trajectory as TrajectoryDO
from vnf.dom.AtomicStructure import StructureTable

# "Holder" in vnf
from ComputationResultTs import ComputationResultTs
Trajectory = o2t(TrajectoryDO, {'subclassFrom': ComputationResultTs}) 



# version
__id__ = "$Id$"

# End of file 
