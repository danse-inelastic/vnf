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

    import dsaw.db
    
    engine = dsaw.db.varchar(name='engine', length=64, default='vasp')
#    engine.validator=dsaw.db.choice(['vasp', 'abinit'])
    engine.meta['tip'] = 'Ab initio engine'
    
    runType = dsaw.db.varchar(name='runType', length=64, default='energy')
    #runType.validator=dsaw.db.choice(['energy', 'optimization', 'md'])
    runType.meta['tip'] = 'Type of run'
    
    xcFunctional = dsaw.db.varchar(name='xcFunctional', length=64, default=['PAW-PBE'])
#    xcFunctional.validator=dsaw.db.choice(['PAW-PBE', 'PAW-GGA', 'LDA'])
    xcFunctional.meta['tip'] = 'Exchange correlation functional'
    
#    xcFunctional = dsaw.db.varcharArray(name='xcFunctional', length=64, default=['PAW-PBE'])
##    xcFunctional.validator=dsaw.db.choice(['PAW-PBE', 'PAW-GGA', 'LDA'])
#    xcFunctional.meta['tip'] = 'Exchange correlation functional'
    
#    KE Cutoff is useful but maybe safer to use well-tested default val and let advanced users set this
#    going to uncomment this temporarily but eventually should be eliminated
    kineticEnergyCutoff = dsaw.db.real(name='kineticEnergyCutoff', default=140.0)
    kineticEnergyCutoff.meta['tip'] = 'Kinetic energy cutoff'
    
    monkhorstPackMesh = dsaw.db.integerArray(name='monkhorstPackMesh', default=[1,1,1])
    monkhorstPackMesh.meta['tip'] = 'Monkhorst pack mesh'



    generateInputsOnly = dsaw.db.boolean(name='generateInputsOnly', default=False)
    

    # meta data:
    DESCRIPTION = "ab initio"
    LONG_DESCRIPTION = [
        "Wikipedia: 'Ab initio quantum chemistry methods are computational chemistry methods based on quantum chemistry. The term ab initio indicates that the calculation is from first principles and that no empirical data is use.'.",
        "In DANSE, we leverage the power of state-of-the-art density functional theory (DFT) codes for  users who want to know what first-principles methods predict about the structure and dynamics of materials.",
        ]
    

# version
__id__ = "$Id$"

# End of file 
