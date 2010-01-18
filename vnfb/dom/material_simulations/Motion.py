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
from vsat.Motion import Motion

# orm

# "Holder" in vnf
from ComputationResult import ComputationResult
MotionTable = o2t(Motion, {'subclassFrom': ComputationResult})

#PhononDOSTable.datafiles = [
#    'data.idf',
#    ]



# version
__id__ = "$Id$"

# End of file 
