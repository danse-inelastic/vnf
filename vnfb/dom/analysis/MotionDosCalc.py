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

from vnfb.dom.Computation import Computation

from vsat.trajectory.MotionDosCalc import MotionDosCalc as MotionDosCalcBase

MotionDosCalc = o2t(MotionDosCalcBase, {'subclassFrom': Computation})
MotionDosCalc.job_builder = 'analysis/motiondoscalc'
MotionDosCalc.actor = 'analysis/motiondoscalc'
MotionDosCalc.result_retriever = 'analysis/motiondoscalc'




# version
__id__ = "$Id$"

# End of file 
