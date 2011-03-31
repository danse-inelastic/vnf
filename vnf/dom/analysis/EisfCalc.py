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
from vsat.trajectory.EisfCalc import EisfCalc as EisfCalcBase

EisfCalc = o2t(EisfCalcBase, {'subclassFrom': Computation})
EisfCalc.job_builder = 'analysiscalc'
EisfCalc.actor = 'analysis/eisfcalc'
EisfCalc.result_retriever = 'eisfcalc'


# version
__id__ = "$Id$"

# End of file 
