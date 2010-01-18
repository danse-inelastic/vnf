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

    len = 0.1
    w = 0.06
    ymin = -0.325
    ymax = 0.325
    nu =600
    delta = 0.0
    tc = 0.0
    nchan = 10
    bw = 0.0005
    blader = 0.5

    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'len', 'w',
            'ymin', 'ymax',
            'nu', 'delta',
            'tc', 'nchan',
            'bw', 'blader',
            ]
    pass


InvBase=base.Inventory
class Inventory(InvBase):


    len = InvBase.d.float(name='len', default=0.1)
    len.tip = 'Slit package length (meter)'
    
    w = InvBase.d.float(name='w', default=0.06)
    w.label = 'width'
    w.tip = 'Slit package width (meter)'
    
    ymin = InvBase.d.float(name='ymin', default=-.0325)
    ymin.tip = 'Lower y bound (meter)'
    
    ymax = InvBase.d.float(name='ymax', default=.0325)
    ymax.tip = 'Upper y bound (meter)'

    nu = InvBase.d.int(name='nu', default=600)
    nu.tip = 'Frequency (Hz)'
    
    delta = InvBase.d.float(name='delta', default=0.0)
    delta.tip = 'time from edge of chopper to center Phase angle (sec)'
    
    tc = InvBase.d.float(name='tc', default=0.0)
    tc.tip = 'time when desired neutron is at the center of the chopper (sec)'
    
    nchan = InvBase.d.int(name='nchan', default=10)
    nchan.tip = 'number of channels in chopper'
    
    bw = InvBase.d.float(name='bw', default=0.0005)
    bw.tip = 'blade width (meter)'
    
    blader = InvBase.d.float(name='blader', default=0.5)    
    blader.tip = 'blade radius (meter)'

    dbtablename = 'fermichoppers'


FermiChopper.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
FermiChopperTable = o2t(FermiChopper, {'subclassFrom': NeutronComponentTableBase})


# version
__id__ = "$Id$"

# End of file 
