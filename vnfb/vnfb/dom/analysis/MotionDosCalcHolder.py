# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import o2t

# still import from vnf-alpha dom. need to change
from vnfb.dom.Computation import Computation

from vsat.trajectory.MotionDosCalc import MotionDosCalc

MotionDosCalcHolder = o2t(MotionDosCalc, {'subclassFrom': Computation, 
                                          'dbtablename':'motiondoscalc'})
MotionDosCalcHolder.job_builder = 'analysis/motiondoscalc'
MotionDosCalcHolder.actor = 'analysis/motiondoscalc'
MotionDosCalcHolder.result_retriever = 'analysis/motiondoscalc'




# version
__id__ = "$Id$"

# End of file 
