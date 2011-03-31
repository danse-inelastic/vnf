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

from vsat.trajectory.SqCalc import SqCalc as SqCalcBase

SqCalc = o2t(SqCalcBase, {'subclassFrom': Computation})
SqCalc.job_builder = 'analysiscalc'
SqCalc.actor = 'analysis/sqcalc'
SqCalc.result_retriever = 'sqcalc'




# version
__id__ = "$Id$"

# End of file 
