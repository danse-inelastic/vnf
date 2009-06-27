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
from GulpPotential import GulpPotential

class GulpSimulation(base):

    name = 'gulpsimulations'
    
    import pyre.db
    
    runtype = pyre.db.varchar(name='runtype', length=64, default='md')
    dos_projections = pyre.db.varcharArray(name='dos_projections', length=32, default=[])
    potential = pyre.db.reference( name='potential', table = GulpPotential)

    # eventually going to get rid of LIBPOINTER_FILE
    CONFIGURATION_FILE = 'gulp.gin'
    LIBPOINTER_FILE = 'gulp.libs'
    datafiles = [
        CONFIGURATION_FILE,
        LIBPOINTER_FILE,
        ]


# version
__id__ = "$Id$"

# End of file 
