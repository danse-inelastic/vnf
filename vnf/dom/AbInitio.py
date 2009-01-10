# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from registry import tableRegistry

from MaterialSimulation import MaterialSimulation as base

class AbInitio(base):

    name = 'abinitio'

    import pyre.db
    
    engine = pyre.db.varchar(name='engine', length=64, default='vasp')
#    engine.validator=pyre.db.choice(['vasp', 'ab init'])
    engine.meta['tip'] = 'Ab initio engine'
    
    xcFunctional = pyre.db.varchar(name='xcFunctional', length=64, default='PAW-PBE')
#    xcFunctional.validator=pyre.db.choice(['PAW-PBE', 'PAW-GGA', 'LDA'])
    xcFunctional.meta['tip'] = 'Exchange correlation functional'
    
    kineticEnergyCutoff = pyre.db.real(name='kineticEnergyCutoff', default=140.0)
    kineticEnergyCutoff.meta['tip'] = 'Kinetic energy cutoff'
    
    monkhorstPackMesh = pyre.db.integerArray(name='monkhorstPackMesh', default=[1,1,1])
    monkhorstPackMesh.meta['tip'] = 'Monkhorst pack mesh'

    generateInputsOnly = pyre.db.boolean(name='generateInputsOnly', default=False)
    

# version
__id__ = "$Id$"

# End of file 
