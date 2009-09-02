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


from registry import tableRegistry
from BvKModel import BvKModel

from MaterialModeling import MaterialModeling as base

class BvKComputation(base):

    name = 'bvkcomputations'

    import pyre.db
    matter = pyre.db.versatileReference(name='matter', tableRegistry=tableRegistry)
                               
    model = pyre.db.reference(name='model', table = BvKModel)
    type = pyre.db.varchar(name='type', length = 16)
    
    dE = pyre.db.real(name='dE', default = 0.5) # unit meV
    N1 = pyre.db.integer(name='N1', default = 10) # number of sampling points (in 1 dimension)


# types of computation
types = [
    ('dos', 'Phonon Density of States'),
    ('directional', 'Phonon dispersion on a special direction'),
    ('disp', 'Full phonon dispersion on a grid (can be used in virtual neutron experiment)'),
    ]

# version
__id__ = "$Id$"

# End of file 
