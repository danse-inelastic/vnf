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
from vnf.dom.Computation import Computation
from vsat.trajectory.IsfCalc import IsfCalc as IsfCalcBase

IsfCalc = o2t(IsfCalcBase, {'subclassFrom': Computation})
IsfCalc.job_builder = 'analysiscalc'
IsfCalc.actor = 'analysis/isfcalc'
IsfCalc.result_retriever = 'analysis/isfcalc'


# version
__id__ = "$Id$"

# End of file 
