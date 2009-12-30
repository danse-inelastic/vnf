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
class T0Chopper(base):

    len = 0.1
    w1 = w2 = 0.06
    ymin = -0.05; ymax = 0.05
    nu = 300
    delta = 0.0
    tc = 0.

    pass



InvBase=base.Inventory
class Inventory(InvBase):

    len = InvBase.d.float(name='len', default=0.1, validator=InvBase.v.positive)
    w1 = InvBase.d.float(name='w1', default=0.06, validator=InvBase.v.positive)
    w2 = InvBase.d.float(name='w2', default=0.06, validator=InvBase.v.positive)
    ymin = InvBase.d.float(name='ymin', default=-.05)
    ymax = InvBase.d.float(name='ymax', default=.05)
    nu = InvBase.d.int(name='nu', default=300, validator=InvBase.v.positive)
    delta = InvBase.d.float(name='delta', default=0.0)
    tc = InvBase.d.float(name='tc', default=0.0)

    dbtablename = 't0choppers'


T0Chopper.Inventory = Inventory
del Inventory


from _ import o2t
T0ChopperTable = o2t(T0Chopper)
    


# version
__id__ = "$Id$"

# End of file 
