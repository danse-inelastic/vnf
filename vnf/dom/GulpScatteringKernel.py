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


from OwnedObject import OwnedObject
class GulpScatteringKernel(OwnedObject):

    name = 'gulpscatteringkernels'
    
    import pyre.db

    inputfile = pyre.db.varcharArray( name = 'inputfile', length = 256 )
    inputfile.meta['tip'] = 'input file to run gulp'



# version
__id__ = "$Id$"

# End of file 
