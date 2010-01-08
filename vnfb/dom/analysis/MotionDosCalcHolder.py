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
from vnfb.dom.Computable import Computable


#from dsaw.model.Inventory import Inventory as InvBase

from vsat.gulp.MotionDosCalc import MotionDosCalc
#from vnfb.dom.AtomicStructure import Structure
#from BvKModel import BvKModel

#class BvKComputation(object):
#
#    model = None
#    matter = None
#
#    class Inventory(InvBase):
#        
#        matter = InvBase.d.reference(name='matter', targettype=None, targettypes=[Structure], owned=0)
#        model = InvBase.d.reference(name='model', targettype = BvKModel, owned=0)
#
#        
#    def isConfigured(self):
#        if self.model is None or self.matter is None: return False
#        return True
#
#
## name of classes must use convention BvK_Get..., see method "getComputationClass"
#
#class BvK_GetDos(BvKComputation):
#
#    df = 0.5
#    N1 = 10
#
#    class Inventory(BvKComputation.Inventory):
#
#        df = InvBase.d.float(name='df', default = 0.1) # unit THz
#        df.tip = 'Frequency axis bin size. unit: THz'
#        N1 = InvBase.d.int(name='N1', default = 10)
#        N1.tip = 'number of sampling points in Q space(in 1 dimension)'
#
#
#    def isConfigured(self):
#        c = super(BvK_GetDos, self).isConfigured()
#        if not c: return c
#
#        if self.df <= 0 or self.N1 <= 0: return False
#        return True
#
#    
#    def customizeLubanObjectDrawer(self, drawer):
#        drawer.sequence = ['properties']
#        drawer.mold.sequence = ['N1', 'df']



MotionDosCalcHolder = o2t(MotionDosCalc, {'subclassFrom': Computable, 'dbtablename':'motiondoscalc'})
MotionDosCalcHolder.job_builder = 'analysis/motiondoscalc'
MotionDosCalcHolder.actor = 'analysis/motiondoscalc'
MotionDosCalcHolder.result_retriever = 'analysis/motiondoscalc'
#def getShortDescription(self):
#    if self.short_description: return self.short_description
#    return 'Compute DOS from BvK model %s: df=%s, N1=%s' % (
#        self.model.id, self.df, self.N1)
#BvK_GetDos_Table.getShortDescription = getShortDescription
#BvK_GetDos_Table.__str__ = getShortDescription



# version
__id__ = "$Id$"

# End of file 
