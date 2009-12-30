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


from AbstractNeutronComponent import AbstractNeutronComponent as base
class ChanneledGuide(base):

    pass # end of ChanneledGuide


InvBase=base.Inventory
class Inventory(InvBase):
    
    w1 = InvBase.d.float(name='w1', default=0.1, validator=InvBase.v.positive)
    h1 = InvBase.d.float(name='h1', default=0.1, validator=InvBase.v.positive)
    w2 = InvBase.d.float(name='w2', default=0.1, validator=InvBase.v.positive)
    h2 = InvBase.d.float(name='h2', default=0.1, validator=InvBase.v.positive)
    l = InvBase.d.float(name='l', default=1)
    R0 = InvBase.d.float(name='R0', default=0.)
    mx = InvBase.d.float(name='mx', default=3.6)
    my = InvBase.d.float(name='my', default=0.1)
    Qcx = InvBase.d.float(name='Qcx', default=0.2)
    Qcy = InvBase.d.float(name='Qcy', default=0.2)
    W = InvBase.d.float(name='W', default=2e-3)
    k = InvBase.d.int(name='k', default=1)
    d = InvBase.d.float(name='d', default=0.)
    alphax = InvBase.d.float(name='alphax', default=0.)
    alphay = InvBase.d.float(name='alphay', default=0.)

    dbtablename = 'channeledguides'

    
ChanneledGuide.Inventory = Inventory
del Inventory


from _ import o2t
ChanneledGuideTable = o2t(ChanneledGuide)



# version
__id__ = "$Id$"

# End of file 
