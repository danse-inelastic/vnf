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
class QEMonitor(base):

    Emin = -50; Emax = 50.; nE = 100
    Qmin = 0; Qmax = 13.; nQ = 130

    max_angle_in_plane = 120.
    min_angle_in_plane = -30.

    max_angle_out_of_plane = 30.
    min_angle_out_of_plane = -30.
    
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    Emin = InvBase.d.float( name = 'Emin', default = -50. )
    Emax = InvBase.d.float( name = 'Emax', default = 50. )
    nE = InvBase.d.int( name = 'nE', default = 100)

    Qmin = InvBase.d.float( name = 'Qmin', default = 0. )
    Qmax = InvBase.d.float( name = 'Qmax', default = 13.  )
    nQ = InvBase.d.int( name = 'nQ', default = 130 )

    max_angle_in_plane = InvBase.d.float(
        name = 'max_angle_in_plane', default = 120. )
    min_angle_in_plane = InvBase.d.float(
        name = 'min_angle_in_plane', default = -30 )
    max_angle_out_of_plane = InvBase.d.float(
        name = 'max_angle_out_of_plane', default = 30 )
    min_angle_out_of_plane = InvBase.d.float(
        name = 'min_angle_out_of_plane', default = -30 )
    
    dbtablename = 'qemonitors'


QEMonitor.Inventory = Inventory
del Inventory


from _ import o2t, MonitorTableBase
QEMonitorTable = o2t(QEMonitor, {'subclassFrom': MonitorTableBase})


# version
__id__ = "$Id$"

# End of file 
