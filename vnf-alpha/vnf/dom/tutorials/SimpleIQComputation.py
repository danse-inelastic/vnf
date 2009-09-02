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


from registry import tableRegistry

from MaterialModeling import MaterialModeling as base

class SimpleIQComputation(base):

    name = 'simpleiqcomputations'

    import dsaw.db
    model = dsaw.db.versatileReference(name='model', tableRegistry=tableRegistry)
    Qmin = dsaw.db.real(name='Qmin', default=0)
    Qmax = dsaw.db.real(name='Qmax', default=10)
    dQ = dsaw.db.real(name='dQ', default=10)


# version
__id__ = "$Id$"

# End of file 
