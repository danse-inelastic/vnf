# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import o2t

# still import from vnf-alpha dom. need to change
from SimulationBase import SimulationBase as SimulationTableBase


from dsaw.model.Inventory import Inventory as InvBase


from vnf.dom.AtomicStructure import Structure
from BvKModel import BvKModel

class BvKComputation(object):

    model = None
    matter = None

    class Inventory(InvBase):
        
        matter = InvBase.d.reference(name='matter', targettype=Structure, owned=0)
        model = InvBase.d.reference(name='model', targettype=BvKModel, owned=0)

        
    def isConfigured(self):
        if self.model is None or self.matter is None: return False
        return True


# name of classes must use convention BvK_Get..., see method "getComputationClass"

class BvK_GetDos(BvKComputation):

    df = 0.02
    N1 = 40

    class Inventory(BvKComputation.Inventory):

        df = InvBase.d.float(name='df', default = 0.02) # unit THz
        df.help = 'Frequency axis bin size. unit: THz'
        df.tip = 'A smaller df means a finer resolution for DOS. You will need a larger N1 to support finer resolution.'
        
        N1 = InvBase.d.int(name='N1', default = 40)
        N1.help = 'number of sampling points in Q space(in 1 dimension)'
        N1.tip = 'DOS is computed from sampling the Brillouin zone. N1**3 is the number of total samples. If you increase N1, you will get a better sampling, but the computation is also more demanding'


    def isConfigured(self):
        c = super(BvK_GetDos, self).isConfigured()
        if not c: return c

        if self.df <= 0 or self.N1 <= 0: return False
        return True

    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = ['N1', 'df']




BvK_GetDos_Table = o2t(BvK_GetDos, {'subclassFrom': SimulationTableBase})
BvK_GetDos_Table.job_builder = 'material_simulations/phonon_calculators/bvk_getdos'
BvK_GetDos_Table.actor = 'material_simulations/phonon_calculators/bvk_getdos'
BvK_GetDos_Table.result_retriever = 'material_simulations/phonon_calculators/bvk_getdos'
def getShortDescription(self):
    if self.short_description: return self.short_description
    return 'Compute DOS from BvK model %s: df=%s, N1=%s' % (
        self.model.id, self.df, self.N1)
BvK_GetDos_Table.getShortDescription = getShortDescription
BvK_GetDos_Table.__str__ = getShortDescription




class BvK_GetPhonons(BvKComputation):

    df = 0.02
    N1 = 40

    class Inventory(BvKComputation.Inventory):

        df = InvBase.d.float(name='df', default = 0.02) # unit THz
        df.help = 'Bin size of frequency axis of density of states curve. unit: THz'
        df.tip = 'A smaller df means a finer resolution for DOS. You will need a larger N1 to support finer resolution.'
        
        N1 = InvBase.d.int(name='N1', default = 40)
        N1.help = 'Number of sampling points in Q space(in 1 dimension)'
        N1.tip = 'DOS is computed from sampling the Brillouin zone. N1**3 is the number of total samples. If you increase N1, you will get a better sampling, but the computation is also more demanding'


    def isConfigured(self):
        c = super(BvK_GetPhonons, self).isConfigured()
        if not c: return c

        if self.df <= 0 or self.N1 <= 0: return False
        return True
    
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = ['N1', 'df']



BvK_GetPhonons_Table = o2t(BvK_GetPhonons, {'subclassFrom': SimulationTableBase})
BvK_GetPhonons_Table.job_builder = 'material_simulations/phonon_calculators/bvk_getphonons'
BvK_GetPhonons_Table.actor = 'material_simulations/phonon_calculators/bvk_getphonons'
BvK_GetPhonons_Table.result_retriever = 'material_simulations/phonon_calculators/bvk_getphonons'
def getShortDescription(self):
    if self.short_description: return self.short_description
    return 'Compute Phonons from BvK model %s: df=%s, N1=%s' % (
        self.model.id, self.df, self.N1)
BvK_GetPhonons_Table.getShortDescription = getShortDescription
BvK_GetPhonons_Table.__str__ = getShortDescription



# targets of computation
targets = [
    ('dos', 'Phonon Density of States'),
    # ('directionalphonons', 'Phonon dispersion on a special direction'),
    ('phonons', 'Phonons on a grid (Good for virtual neutron experiments)'),
    ]


def getComputationClass(target):
    return eval('BvK_Get%s' % target.capitalize())


def getComputations():
    'return a list of bvk computation types'
    return [getComputationClass(t) for t, d in targets]


# version
__id__ = "$Id$"

# End of file 
