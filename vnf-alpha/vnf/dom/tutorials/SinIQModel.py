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

    import dsaw.db
    bg = dsaw.db.real(name='bg', default=0)
    amplitude = dsaw.db.real(name='amplitude', default=0)
    L = dsaw.db.real(name='L', default=0)
    phase = dsaw.db.real(name='phase', default=0)



# version
__id__ = "$Id$"

# End of file 
