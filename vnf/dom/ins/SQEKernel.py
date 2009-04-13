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

from ScatteringKernel import ScatteringKernel as base
class SQEKernel(base):

    name = 'polyxtalcoherentphononscatteringkernels'
    
    import pyre.db

    sqe = pyre.db.versatileReference(name = 'sqe', tableRegistry=tableRegistry)

    Qmin = pyre.db.real(name = 'Qmin', default = 0)
    Qmax = pyre.db.real(name = 'Qmax', default = 10)

    Emin = pyre.db.real(name = 'Emin', default = -50)
    Emax = pyre.db.real(name = 'Emax', default = 50)
    
    pass # end of SQEKernel



# version
__id__ = "$Id$"

# End of file 
