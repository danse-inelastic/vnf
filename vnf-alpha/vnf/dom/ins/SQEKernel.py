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

    name = 'sqekernels'
    
    import dsaw.db

    sqe = dsaw.db.versatileReference(name = 'sqe')

    Qmin = dsaw.db.real(name = 'Qmin', default = 0)
    Qmax = dsaw.db.real(name = 'Qmax', default = 10)

    Emin = dsaw.db.real(name = 'Emin', default = -50)
    Emax = dsaw.db.real(name = 'Emax', default = 50)
    
    pass # end of SQEKernel



# version
__id__ = "$Id$"

# End of file 
