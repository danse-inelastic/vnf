# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from OwnedObject import OwnedObject as base

class SinIQModel(base):

    '''bg + amplitude * sin(L*q + phase)**2
    '''
    
    name = 'siniqmodels'

    import pyre.db
    bg = pyre.db.float(name='bg', default=0)
    amplitude = pyre.db.float(name='amplitude', default=0)
    L = pyre.db.float(name='L', default=0)
    phase = pyre.db.float(name='phase', default=0)



# version
__id__ = "$Id$"

# End of file 
