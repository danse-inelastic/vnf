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
from vsat.trajectory.CsfCalc import CsfCalc as CsfCalcBase

CsfCalc = o2t(CsfCalcBase, {'subclassFrom': Computation})
CsfCalc.job_builder = 'analysis/csfcalc'
CsfCalc.actor = 'analysis/csfcalc'
CsfCalc.result_retriever = 'analysis/csfcalc'


# version
__id__ = "$Id$"

# End of file 
