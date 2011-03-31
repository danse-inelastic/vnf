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
from AbstractNeutronComponent import AbstractNeutronComponent as base
class CollimatorLinear(base):
    abstract = False
    x_min = 0
    x_max = 0
    y_min = 0
    y_max = 0
    len = 0
    divergence = 40.0
    transmission = 1.0
    divergenceV = 0.0
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = ['componentname', 'short_description', 'referencename', 'position', 'orientation', 'x_min', 'x_max', 'y_min', 'y_max', 'len', 'divergence', 'transmission', 'divergenceV']
InvBase=base.Inventory
class Inventory(InvBase):
    x_min = InvBase.d.float(name='x_min', default=0)
    x_min.help = '(m)              Lower x bound on slits'
    x_max = InvBase.d.float(name='x_max', default=0)
    x_max.help = '(m)              Upper x bound on slits'
    y_min = InvBase.d.float(name='y_min', default=0)
    y_min.help = '(m)              Lower y bound on slits'
    y_max = InvBase.d.float(name='y_max', default=0)
    y_max.help = '(m)              Upper y bound on slits'
    len = InvBase.d.float(name='len', default=0)
    len.help = '(m)              Distance between slits'
    divergence = InvBase.d.float(name='divergence', default=40.0)
    divergence.help = '(minutes of arc) Divergence horizontal angle (calculated as atan(d/len),'
    transmission = InvBase.d.float(name='transmission', default=1.0)
    transmission.help = '(1)              Transmission of Soller (0<=t<=1)'
    divergenceV = InvBase.d.float(name='divergenceV', default=0.0)
    divergenceV.help = '(minutes of arc) Divergence vertical angle'
    dbtablename = 'collimatorlinears'
CollimatorLinear.Inventory = Inventory
del Inventory
from _ import o2t, NeutronComponentTableBase
CollimatorLinearTable = o2t(CollimatorLinear, {'subclassFrom': NeutronComponentTableBase})
# version
__id__ = "$Id$"

# End of file 
