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

from OwnedObject import OwnedObject as base

class BvKComputation(base):

    name = 'bvkcomputations'

    import pyre.db
    matter = pyre.db.versatileReference(name='matter', tableRegistry=tableRegistry)
                               
    model = pyre.db.reference(name='model', table = BvKModel)
    type = pyre.db.varchar(name='type', length = 16)
    dE = pyre.db.real(name='dE', default = 0.5) # unit meV
    Qs = pyre.db.versatileReference(name='Qs', tableRegistry = tableRegistry)

    import vnf.dom
    results = vnf.dom.referenceSet(name='results')
    

# version
__id__ = "$Id$"

# End of file 
