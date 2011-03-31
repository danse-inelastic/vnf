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

from vsat.trajectory.MdDosCalc import MdDosCalc as MdDosCalcBase

MdDosCalc = o2t(MdDosCalcBase, {'subclassFrom': Computation})
MdDosCalc.job_builder = 'analysiscalc'
MdDosCalc.actor = 'analysis/mddoscalc'
MdDosCalc.result_retriever = 'mddoscalc'




# version
__id__ = "$Id$"

# End of file 
