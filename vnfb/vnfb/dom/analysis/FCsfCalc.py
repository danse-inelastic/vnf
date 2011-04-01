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
from vsat.trajectory.FCsfCalc import FCsfCalc as FCsfCalcBase

FCsfCalc = o2t(FCsfCalcBase, {'subclassFrom': Computation, 'dbtablename':'fcsfcalc'})
FCsfCalc.job_builder = 'analysiscalc'
FCsfCalc.actor = 'analysis/fcsfcalc'
FCsfCalc.result_retriever = 'fcsfcalc'


# version
__id__ = "$Id$"

# End of file 
