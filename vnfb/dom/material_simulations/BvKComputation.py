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
from Computation import Computation as ComputationTableBase


from dsaw.model.Inventory import Inventory as InvBase


from vnfb.dom.AtomicStructure import Structure
from BvKModel import BvKModel

class BvKComputation(object):

    class Inventory(InvBase):
        
        matter = InvBase.d.reference(name='matter', targettype=None, targettypes=[Structure], owned=0)
        model = InvBase.d.reference(name='model', targettype = BvKModel, owned=0)
        


# name of classes must use convention BvK_Get..., see method "getComputationClass"

class BvK_GetDos(BvKComputation):

    df = 0.5
    N1 = 10

    class Inventory(BvKComputation.Inventory):

        df = InvBase.d.float(name='df', default = 0.5) # unit THz
        df.tip = 'Frequency axis bin size. unit: THz'
        N1 = InvBase.d.int(name='N1', default = 10)
        N1.tip = 'number of sampling points in Q space(in 1 dimension)'

    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties']
        drawer.mold.sequence = ['N1', 'df']


BvK_GetDos_Table = o2t(BvK_GetDos, {'subclassFrom': ComputationTableBase})
BvK_GetDos_Table.job_builder = 'material_simulations/phonon_calculators/bvk_getdos'


# targets of computation
targets = [
    ('dos', 'Phonon Density of States'),
    ('directionaldispersion', 'Phonon dispersion on a special direction'),
    ('dispersion', 'Full phonon dispersion on a grid (can be used in virtual neutron experiment)'),
    ]


def getComputationClass(target):
    return eval('BvK_Get%s' % target.capitalize())


# version
__id__ = "$Id$"

# End of file 
