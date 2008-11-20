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
class ChanneledGuide(base):

    name = 'channeledguides'

    import pyre.db

    w1 = pyre.db.real(name='w1', default=0.1)
    h1 = pyre.db.real(name='h1', default=0.1)
    w2 = pyre.db.real(name='w2', default=0.1)
    h2 = pyre.db.real(name='h2', default=0.1)
    l = pyre.db.real(name='l', default=1)
    R0 = pyre.db.real(name='R0', default=0.)
    mx = pyre.db.real(name='mx', default=3.6)
    my = pyre.db.real(name='my', default=0.1)
    Qcx = pyre.db.real(name='Qcx', default=0.2)
    Qcy = pyre.db.real(name='Qcy', default=0.2)
    W = pyre.db.real(name='W', default=2e-3)
    k = pyre.db.integer(name='k', default=1)
    d = pyre.db.real(name='d', default=0.)
    alphax = pyre.db.real(name='alphax', default=0.)
    alphay = pyre.db.real(name='alphay', default=0.)

    pass # end of ChanneledGuide


# version
__id__ = "$Id$"

# End of file 
