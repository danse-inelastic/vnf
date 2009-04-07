# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from MaterialSimulation import MaterialSimulation as base
class MdAnalysis(base):

    name = 'mdanalysis'
    
    import pyre.db
    
#    supercell = pyre.db.integerArray(name='supercell', default=[1,1,1])
#    supercell.meta['tip'] = 'Supercell for phonon calculation'
#    
#    displacementAmplitude = pyre.db.real(name='displacementAmplitude', default=0.01)
#    displacementAmplitude.meta['tip'] = 'Displacement amplitude'      
#    
#    qGrid = pyre.db.integerArray(name='qGrid', default=[1,1,1])
#    qGrid.meta['tip'] = 'Q grid for phonon calculation'
#
#    abinitio = pyre.db.reference(name='abinitio', table = AbInitio)
#
#    CONFIGURATION_FILE = 'gulp.gin'
#    LIBPOINTER_FILE = 'gulp.libs'
#    datafiles = [
#        CONFIGURATION_FILE,
#        LIBPOINTER_FILE,
#        ]


# version
__id__ = "$Id$"

# End of file 
