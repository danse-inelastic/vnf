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

    import dsaw.db

    w1 = dsaw.db.real(name='w1', default=0.1)
    h1 = dsaw.db.real(name='h1', default=0.1)
    w2 = dsaw.db.real(name='w2', default=0.1)
    h2 = dsaw.db.real(name='h2', default=0.1)
    l = dsaw.db.real(name='l', default=1)
    R0 = dsaw.db.real(name='R0', default=0.)
    mx = dsaw.db.real(name='mx', default=3.6)
    my = dsaw.db.real(name='my', default=0.1)
    Qcx = dsaw.db.real(name='Qcx', default=0.2)
    Qcy = dsaw.db.real(name='Qcy', default=0.2)
    W = dsaw.db.real(name='W', default=2e-3)
    k = dsaw.db.integer(name='k', default=1)
    d = dsaw.db.real(name='d', default=0.)
    alphax = dsaw.db.real(name='alphax', default=0.)
    alphay = dsaw.db.real(name='alphay', default=0.)

    pass # end of ChanneledGuide


# version
__id__ = "$Id$"

# End of file 
