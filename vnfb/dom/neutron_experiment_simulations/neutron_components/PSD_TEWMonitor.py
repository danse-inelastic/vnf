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
from MonitorBase import MonitorBase as base
class PSD_TEWMonitor(base):

    abstract = False
    nxchan = 20.0
    nychan = 20.0
    nbchan = 20.0
    type = 'time'
    format = 'table'
    x_width = 0.0
    y_height = 0.0
    bmin = 0.0
    bmax = 0.0
    deltab = 0.0
    restore_neutron = 0.0
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = ['componentname', 'short_description', 'referencename', 'position', 'orientation', 'nxchan', 'nychan', 'nbchan', 'type', 'format', 'x_width', 'y_height', 'bmin', 'bmax', 'deltab', 'restore_neutron']
InvBase=base.Inventory
class Inventory(InvBase):
    nxchan = InvBase.d.float(name='nxchan', default=20.0)
    nxchan.help = 'Number of x bins (1)'
    nychan = InvBase.d.float(name='nychan', default=20.0)
    nychan.help = 'Number of x bins (1)'
    nbchan = InvBase.d.float(name='nbchan', default=20.0)
    nbchan.help = 'Number of tow bins (1)'
    type = InvBase.d.str(name='type', default='time')
    type.help = 'detector type "time"/"energy"/"wavelength" (string)'
    format = InvBase.d.str(name='format', default='table')
    format.help = '"table"- binned values on ascii file; "detector_out"- McStas format ascii'
    x_width = InvBase.d.float(name='x_width', default=0.0)
    x_width.help = 'Width/diameter of detector (x). Overrides x_min,x_max. (m)'
    y_height = InvBase.d.float(name='y_height', default=0.0)
    y_height.help = 'Height of detector (y). Overrides y_min,y_max. (m)'
    bmin = InvBase.d.float(name='bmin', default=0.0)
    bmin.help = 'Lower time/energy/wavelength limit (ms/meV/AA)'
    bmax = InvBase.d.float(name='bmax', default=0.0)
    bmax.help = 'Upper time/energy/wavelength limit (ms/meV/AA)'
    deltab = InvBase.d.float(name='deltab', default=0.0)
    deltab.help = 'time/energy/wavelength bin width'
    restore_neutron = InvBase.d.float(name='restore_neutron', default=0.0)
    restore_neutron.help = 'If set >0, the monitor does not influence the neutron state'
    dbtablename = 'psd_tewmonitors'
PSD_TEWMonitor.Inventory = Inventory
del Inventory
from _ import o2t, MonitorTableBase
PSD_TEWMonitorTable = o2t(PSD_TEWMonitor, {'subclassFrom': MonitorTableBase})
# version
__id__ = "$Id$"

# End of file 
