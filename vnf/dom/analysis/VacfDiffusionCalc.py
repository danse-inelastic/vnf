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

from vnf.dom.Computation import Computation

from vsat.trajectory.VacfDiffusionCalc import VacfDiffusionCalc as VacfDiffusionCalcBase

VacfDiffusionCalc = o2t(VacfDiffusionCalcBase, {'subclassFrom': Computation})
VacfDiffusionCalc.job_builder = 'analysiscalc'
VacfDiffusionCalc.actor = 'analysis/vacfdiffusioncalc'
VacfDiffusionCalc.result_retriever = 'vacfdiffusioncalc'




# version
__id__ = "$Id$"

# End of file 
