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

    pass


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    Emin = InvBase.d.float( name = 'Emin', default = 10 )
    Emax = InvBase.d.float( name = 'Emax', default = 100 )
    x_min = InvBase.d.float( name = 'x_min', default = -0.1 )
    x_max = InvBase.d.float( name = 'x_max', default = 0.1 )
    y_min = InvBase.d.float( name = 'y_min', default = -0.1 )
    y_max = InvBase.d.float( name = 'y_max', default = 0.1 )
    
    nchan = InvBase.d.int( name = 'nchan', default = 100, validator=InvBase.v.positive)
    
    dbtablename = 'emonitors'


EMonitor.Inventory = Inventory
del Inventory


from _ import o2t
EMonitorTable = o2t(EMonitor)


# version
__id__ = "$Id$"

# End of file 
