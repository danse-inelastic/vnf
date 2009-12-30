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
class FermiChopper(base):

    pass


InvBase=base.Inventory
class Inventory(InvBase):

    len = InvBase.d.float(name='len', default=0.1)
    w = InvBase.d.float(name='w', default=0.06)
    ymin = InvBase.d.float(name='ymin', default=-.0325)
    ymax = InvBase.d.float(name='ymax', default=.0325)
    nu = InvBase.d.int(name='nu', default=600)
    delta = InvBase.d.float(name='delta', default=0.0)
    tc = InvBase.d.float(name='tc', default=0.0)
    nchans = InvBase.d.int(name='nchans', default=10)
    bw = InvBase.d.float(name='bw', default=0.0005)
    blader = InvBase.d.float(name='blader', default=0.5)    

    dbtablename = 'fermichoppers'


FermiChopper.Inventory = Inventory
del Inventory


from _ import o2t
FermiChopperTable = o2t(FermiChopper)


# version
__id__ = "$Id$"

# End of file 
