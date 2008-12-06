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


from Computation import Computation as base
class GulpSimulation(base):

    name = 'gulpsimulations'
    
    import pyre.db
    
    datafiles = [
        'gulp.gin', 
        #'gulp.lib',
        ]


# version
__id__ = "$Id$"

# End of file 
