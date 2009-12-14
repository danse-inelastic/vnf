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


from dsaw.model.Inventory import Inventory as InvBase


from vnfb.dom.AtomicStructure import Structure
from BvKModel import BvKModel

class BvKComputation(object):

    class Inventory(InvBase):
        
        matter = InvBase.d.reference(name='matter', targettype=None, targettypes=[Structure], owned=0)
        model = InvBase.d.reference(name='model', targettype = BvKModel, owned=0)
        

class BvKComputation_GetDOS(BvKComputation):

    class Inventory(InvBase):

        dE = InvBase.d.float(name='dE', default = 0.5) # unit meV
        N1 = InvBase.d.int(name='N1', default = 10) # number of sampling points (in 1 dimension)


# targets of computation
targets = [
    ('dos', 'Phonon Density of States'),
    ('directionaldispersion', 'Phonon dispersion on a special direction'),
    ('dispersion', 'Full phonon dispersion on a grid (can be used in virtual neutron experiment)'),
    ]


# version
__id__ = "$Id$"

# End of file 
