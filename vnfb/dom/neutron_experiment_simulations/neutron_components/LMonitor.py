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
class LMonitor(base):

    abstract = False

    Lmin = 2.
    Lmax = 10.
    x_min = y_min = 0
    x_max = y_max = 0
    x_width = y_height = 0 #0.15
    nchan = 100

    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'Lmin', 'Lmax', 'nchan',
            'x_min', 'x_max',
            'y_min', 'y_max',
            'x_width', 'y_height',
            ]
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    # 9 total
    Lmin = InvBase.d.float( name = 'Lmin', default = 2, validator=InvBase.v.positive)
    Lmin.help = 'Minimum wavelength to detect (AA) '
    Lmax = InvBase.d.float( name = 'Lmax', default = 10, validator=InvBase.v.positive)
    Lmax.help = 'Maximum wavelength to detect (AA) '
    x_min = InvBase.d.float( name = 'x_min', default = 0 )
    x_min.help = 'Lower x bound of detector opening (m) '
    x_max = InvBase.d.float( name = 'x_max', default = 0 )
    x_max.help = 'Upper x bound of detector opening (m) '
    y_min = InvBase.d.float( name = 'y_min', default = 0 )
    y_min.help = 'Lower y bound of detector opening (m) '
    y_max = InvBase.d.float( name = 'y_max', default = 0 )
    y_max.help = 'Upper y bound of detector opening (m) '
    x_width = InvBase.d.float( name = 'x_width', default = 0, validator=InvBase.v.positive )
    x_width.help = 'Width/diameter of detector (x). Overrides xmin,xmax. (m) '
    y_height = InvBase.d.float( name = 'y_height', default = 0, validator=InvBase.v.positive )
    y_height.help = 'Height of detector (y). Overrides ymin,ymax. (m) '


    nchan = InvBase.d.int( name = 'nchan', default = 100, validator=InvBase.v.positive)
    nchan.help = 'Number of wavelength channels (1) '

    dbtablename = 'lmonitors'


LMonitor.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
LMonitorTable = o2t(LMonitor, {'subclassFrom': MonitorTableBase})


__date__ = "$Sep 12, 2010 12:19:20 AM$"


