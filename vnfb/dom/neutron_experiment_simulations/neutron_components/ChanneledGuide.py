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
class ChanneledGuide(base):

    abstract = False
    
    w1 = 0.10000000000000001
    h1 = 0.12
    w2 = 0.02
    h2 = 0.02
    l = 2.0
    R0 = 0.98999999999999999
    Qcx = 0.021000000000000001
    Qcy = 0.021000000000000001
    alphax = 6.0700000000000003
    alphay = 6.0700000000000003
    W = 0.0030000000000000001
    k = 1.0
    d = 0.00050000000000000001
    mx = 1.0
    my = 1.0
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = ['componentname', 'short_description', 'referencename', 'position', 'orientation', 'w1', 'h1', 'w2', 'h2', 'l', 'R0', 'Qcx', 'Qcy', 'alphax', 'alphay', 'W', 'k', 'd', 'mx', 'my']
InvBase=base.Inventory
class Inventory(InvBase):
    w1 = InvBase.d.float(name='w1', default=0.10000000000000001)
    w1.help = '(m) Width at the guide entry '
    h1 = InvBase.d.float(name='h1', default=0.12)
    h1.help = '(m) Height at the guide entry '
    w2 = InvBase.d.float(name='w2', default=0.02)
    w2.help = '(m) Width at the guide exit '
    h2 = InvBase.d.float(name='h2', default=0.02)
    h2.help = '(m) Height at the guide exit '
    l = InvBase.d.float(name='l', default=2.0)
    l.help = '(m) Length of guide '
    R0 = InvBase.d.float(name='R0', default=0.98999999999999999)
    R0.help = '(1) Low-angle reflectivity '
    Qcx = InvBase.d.float(name='Qcx', default=0.021000000000000001)
    Qcx.help = '(AA-1) Critical scattering vector for left and right vertical mirrors in each channel'
    Qcy = InvBase.d.float(name='Qcy', default=0.021000000000000001)
    Qcy.help = '(AA-1) Critical scattering vector for top and bottom mirrors '
    alphax = InvBase.d.float(name='alphax', default=6.0700000000000003)
    alphax.help = '(AA) Slope of reflectivity for left and right vertical mirrors in each channel'
    alphay = InvBase.d.float(name='alphay', default=6.0700000000000003)
    alphay.help = '(AA) Slope of reflectivity for top and bottom mirrors '
    W = InvBase.d.float(name='W', default=0.0030000000000000001)
    W.help = '(AA-1) Width of supermirror cut-off for all mirrors '
    k = InvBase.d.float(name='k', default=1.0)
    k.help = '(1) Number of channels in the guide (>= 1) '
    d = InvBase.d.float(name='d', default=0.00050000000000000001)
    d.help = '(m) Thickness of subdividing walls '
    mx = InvBase.d.float(name='mx', default=1.0)
    mx.help = '(1) m-value of material for left and right vertical mirrors in each channel. Zero means completely absorbing.'
    my = InvBase.d.float(name='my', default=1.0)
    my.help = '(1) m-value of material for top and bottom mirrors. Zero means completely absorbing.'
    dbtablename = 'channeledguides'
ChanneledGuide.Inventory = Inventory
del Inventory
from _ import o2t, NeutronComponentTableBase
ChanneledGuideTable = o2t(ChanneledGuide, {'subclassFrom': NeutronComponentTableBase})
# version
__id__ = "$Id$"

# End of file 
