# -*- Python -*-
# auto-generated by mcstas-component-to-dom
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
from AbstractNeutronComponent import AbstractNeutronComponent as base
class T0Chopper(base):

    abstract = False

    len = 0.0
    w1 = 0.0
    w2 = 0.0
    nu = 0.0
    delta = 0.0
    tc = 0.0
    ymin = 0.0
    ymax = 0.0
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = ['componentname', 'short_description', 'referencename', 'position', 'orientation', 'len', 'w1', 'w2', 'nu', 'delta', 'tc', 'ymin', 'ymax']
InvBase=base.Inventory
class Inventory(InvBase):
    len = InvBase.d.float(name='len', default=0.0)
    len.help = 'length of slot (m) '
    w1 = InvBase.d.float(name='w1', default=0.0)
    w1.help = 'center width (m) '
    w2 = InvBase.d.float(name='w2', default=0.0)
    w2.help = 'edgewidth '
    nu = InvBase.d.float(name='nu', default=0.0)
    nu.help = 'frequency (Hz) '
    delta = InvBase.d.float(name='delta', default=0.0)
    delta.help = 'time from edge of chopper to center Phase angle (sec) '
    tc = InvBase.d.float(name='tc', default=0.0)
    tc.help = 'time when desired neutron is at the center of the chopper (sec) '
    ymin = InvBase.d.float(name='ymin', default=0.0)
    ymin.help = 'Lower y bound (m) '
    ymax = InvBase.d.float(name='ymax', default=0.0)
    ymax.help = 'Upper y bound (m) '
    dbtablename = 't0choppers'
T0Chopper.Inventory = Inventory
del Inventory
from _ import o2t, NeutronComponentTableBase
T0ChopperTable = o2t(T0Chopper, {'subclassFrom': NeutronComponentTableBase})
# version
__id__ = "$Id$"

# End of file 