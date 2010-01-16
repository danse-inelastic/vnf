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


from Monitor import Monitor as base
class EMonitor(base):

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
    Emax = InvBase.d.float( name = 'Emax', default = 100, validator=InvBase.v.positive)
    x_min = InvBase.d.float( name = 'x_min', default = -0.1 )
    x_max = InvBase.d.float( name = 'x_max', default = 0.1 )
    y_min = InvBase.d.float( name = 'y_min', default = -0.1 )
    y_max = InvBase.d.float( name = 'y_max', default = 0.1 )
    
    nchan = InvBase.d.int( name = 'nchan', default = 100, validator=InvBase.v.positive)
    
    dbtablename = 'emonitors'


EMonitor.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
EMonitorTable = o2t(EMonitor, {'subclassFrom': MonitorTableBase})


# version
__id__ = "$Id$"

# End of file 
