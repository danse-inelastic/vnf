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


from NeutronComponent import NeutronComponent as base
class T0Chopper(base):

    name = 't0choppers'

    import pyre.db

    len = pyre.db.real(name='len', default=0.1)
    w1 = pyre.db.real(name='w1', default=0.06)
    w2 = pyre.db.real(name='w2', default=0.06)
    ymin = pyre.db.real(name='ymin', default=-.05)
    ymax = pyre.db.real(name='ymax', default=.05)
    nu = pyre.db.integer(name='nu', default=300)
    delta = pyre.db.real(name='delta', default=0.0)
    tc = pyre.db.real(name='tc', default=0.0)

    pass # end of T0Chopper


# version
__id__ = "$Id$"

# End of file 
