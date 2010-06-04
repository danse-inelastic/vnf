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

from vsat.trajectory.VacfCalc import VacfCalc as VacfCalcBase

VacfCalc = o2t(VacfCalcBase, {'subclassFrom': Computation})
VacfCalc.job_builder = 'analysiscalc'
VacfCalc.actor = 'analysis/vacfcalc'
VacfCalc.result_retriever = 'vacfcalc'




# version
__id__ = "$Id$"

# End of file 
