# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from MonitorBase import MonitorBase as base
class VulcanDetectorSystem(base):

    abstract    = False
    
    tmin        = 0
    tmax        = 0.1
    nt          = 100
    wmin        = 0
    wmax        = 10
    nw          = 100
    xwidth      = 0.770
    yheight     = 0.385

    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'tmin', 'tmax', 'nt',
            'wmin', 'wmax', 'nw',
            'xwidth', 'yheight'
            ]

InvBase=base.Inventory
class Inventory(InvBase):

    tmin        = InvBase.d.float(name='tmin', default=0., validator=InvBase.v.positive)
    tmin.tip    = 'Minimum TOF, seconds'
    tmin.help   = tmin.tip

    tmax        = InvBase.d.float(name='tmax', default=0.1, validator=InvBase.v.positive)
    tmax.tip    = 'Maximum TOF, seconds'
    tmax.help   = tmax.tip

    nt          = InvBase.d.int(name='nt', default=100, validator=InvBase.v.positive)
    nt.tip      = 'Number of divisions in time axes'
    nt.help     = nt.tip

    wmin        = InvBase.d.float(name='wmin', default=0., validator=InvBase.v.positive)
    wmin.tip    = 'Minimum of wavelength, AA'
    wmin.help   = wmin.tip

    wmax        = InvBase.d.float(name='wmax', default=10., validator=InvBase.v.positive)
    wmax.tip    = 'Maximum of wavelength, AA'
    wmax.help   = wmax.tip
    
    nw          = InvBase.d.int(name='nw', default=100, validator=InvBase.v.positive)
    nw.tip      = 'Number of divisions in wavelength axes'
    nw.help     = nw.tip
    
    xwidth      = InvBase.d.float(name='xwidth', default=0.770, validator=InvBase.v.positive)
    xwidth.tip  = 'Width of monitors, m'
    xwidth.help = xwidth.tip

    yheight     = InvBase.d.float(name='yheight', default=0.385, validator=InvBase.v.positive)
    yheight.tip = 'Height of monitors, m'
    yheight.help = yheight.tip

    dbtablename = 'vulcan_detector_system'

VulcanDetectorSystem.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
VulcanDetectorSystemTable = o2t(VulcanDetectorSystem, {'subclassFrom': MonitorTableBase})

__date__ = "$Mar 8, 2011 11:57:08 AM$"


