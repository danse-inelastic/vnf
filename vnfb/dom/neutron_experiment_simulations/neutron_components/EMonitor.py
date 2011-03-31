# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from MonitorBase import MonitorBase as base
class EMonitor(base):

    abstract = False

    Emin = 10.
    Emax = 100.
    x_min = y_min = -0.1
    x_max = y_max = 0.1
    nchan = 100
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'Emin', 'Emax', 'nchan',
            'x_min', 'x_max',
            'y_min', 'y_max',
            ]
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    Emin = InvBase.d.float( name = 'Emin', default = 10, validator=InvBase.v.positive)
    Emin.help = 'Minimum energy to detect (meV) '
    Emax = InvBase.d.float( name = 'Emax', default = 100, validator=InvBase.v.positive)
    Emax.help = 'Maximum energy to detect (meV) '
    x_min = InvBase.d.float( name = 'x_min', default = -0.1 )
    x_min.help = 'Lower x bound of detector opening (m) '
    x_max = InvBase.d.float( name = 'x_max', default = 0.1 )
    x_max.help = 'Upper x bound of detector opening (m) '
    y_min = InvBase.d.float( name = 'y_min', default = -0.1 )
    y_min.help = 'Lower y bound of detector opening (m) '
    y_max = InvBase.d.float( name = 'y_max', default = 0.1 )
    y_max.help = 'Upper y bound of detector opening (m) '
    
    nchan = InvBase.d.int( name = 'nchan', default = 100, validator=InvBase.v.positive)
    nchan.help = 'Number of energy channels (1) '

    dbtablename = 'emonitors'


EMonitor.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
EMonitorTable = o2t(EMonitor, {'subclassFrom': MonitorTableBase})


# version
__id__ = "$Id$"

# End of file 
