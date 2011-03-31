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

from vsat.trajectory.MsdDiffusionCalc import MsdDiffusionCalc as MsdDiffusionCalcBase

MsdDiffusionCalc = o2t(MsdDiffusionCalcBase, {'subclassFrom': Computation})
MsdDiffusionCalc.job_builder = 'analysiscalc'
MsdDiffusionCalc.actor = 'analysis/msddiffusioncalc'
MsdDiffusionCalc.result_retriever = 'msddiffusioncalc'




# version
__id__ = "$Id$"

# End of file 
