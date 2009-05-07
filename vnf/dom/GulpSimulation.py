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
class GulpSimulation(base):

    name = 'gulpsimulations'
    
    import pyre.db
    
    runtype = pyre.db.varchar(name='runtype', length=64, default='md')

    CONFIGURATION_FILE = 'gulp.gin'
    LIBPOINTER_FILE = 'gulp.libs'
    datafiles = [
        CONFIGURATION_FILE,
        LIBPOINTER_FILE,
        ]


# version
__id__ = "$Id$"

# End of file 
