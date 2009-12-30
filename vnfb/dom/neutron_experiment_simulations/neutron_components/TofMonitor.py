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


from Monitor import Monitor as base
class TofMonitor(base):

    tmin = 3000e-6
    tmax = 6000e-6
    x_min = -0.1
    x_max = 0.1
    y_min = -0.1
    y_max = 0.1
    nchan = 100

    pass


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    tmin = InvBase.d.float( name = 'tmin', default = 3000e-6 )
    tmax = InvBase.d.float( name = 'tmax', default = 6000e-6  )
    x_min = InvBase.d.float( name = 'x_min', default = -0.1 )
    x_max = InvBase.d.float( name = 'x_max', default = 0.1 )
    y_min = InvBase.d.float( name = 'y_min', default = -0.1 )
    y_max = InvBase.d.float( name = 'y_max', default = 0.1 )
    
    nchan = InvBase.d.int( name = 'nchan', default = 100, validator=InvBase.v.positive)

    dbtablename = 'tofmonitors'


TofMonitor.Inventory = Inventory
del Inventory


from _ import o2t
TofMonitorTable = o2t(TofMonitor)


# version
__id__ = "$Id$"

# End of file 
