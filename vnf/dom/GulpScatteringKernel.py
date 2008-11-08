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


from ScatteringKernel import ScatteringKernel as base
class GulpScatteringKernel(base):

    name = 'gulpscatteringkernels'
    
    import pyre.db

# change input file to description (and add any other metadata necessary

    inputfile = pyre.db.varcharArray( name = 'inputfile', length = 256 )
    inputfile.meta['tip'] = 'input file to run gulp'



# version
__id__ = "$Id$"

# End of file 
