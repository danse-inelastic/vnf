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


from MonitorBase import MonitorBase as base
class TofMonitor(base):

    abstract = False

    tmin = 3000e-6
    tmax = 6000e-6
    x_min = -0.1
    x_max = 0.1
    y_min = -0.1
    y_max = 0.1
    nchan = 100

    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'tmin', 'tmax', 'nchan',
            'x_min', 'x_max',
            'y_min', 'y_max',
            ]

    pass


InvBase=base.Inventory
class Inventory(InvBase):

    tmin = InvBase.d.float( name = 'tmin', default = 3000e-6 )
    tmin.help = 'lower t bound of detector (s) '
    tmax = InvBase.d.float( name = 'tmax', default = 6000e-6  )
    tmax.help = 'upper t bound of detector (s) '
    x_min = InvBase.d.float( name = 'x_min', default = -0.1 )
    x_min.help = 'Lower x bound of detector opening (m) '
    x_max = InvBase.d.float( name = 'x_max', default = 0.1 )
    x_max.help = 'Upper x bound of detector opening (m) '
    y_min = InvBase.d.float( name = 'y_min', default = -0.1 )
    y_min.help = 'Lower y bound of detector opening (m) '
    y_max = InvBase.d.float( name = 'y_max', default = 0.1 )
    y_max.help = 'Upper y bound of detector opening (m) '
    
    nchan = InvBase.d.int( name = 'nchan', default = 100, validator=InvBase.v.positive)
    nchan.help = 'number of time bins (1) '

    dbtablename = 'tofmonitors'


TofMonitor.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
TofMonitorTable = o2t(TofMonitor, {'subclassFrom': MonitorTableBase})


# version
__id__ = "$Id$"

# End of file 
