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

from AbstractNeutronComponent import AbstractNeutronComponent as base
class SimpleSource(base):

    abstract = False

    radius  = 0
    height  = 0.1
    width   = 0.1
    dist    = 3.
    xw      = 0.1
    yh      = 0.1
    E0      = 70
    dE      = 50
    Lambda0 = 0
    dLambda = 0
    flux    = 1
    gauss   = 0


    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'radius', 'height', 'width', 'dist',
            'xw', 'yh', 'E0', 'dE', 'Lambda0',
            'dLambda', 'flux', 'gauss'
            ]
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    radius = InvBase.d.float( name = 'radius', default = 0., validator=InvBase.v.nonnegative)
    radius.help = 'm, Radius of circle in (x,y,0) plane where neutrons are generated'

    height = InvBase.d.float( name = 'height', default = 0.1, validator=InvBase.v.nonnegative)
    height.help = 'm, Height of rectangle in (x,y,0) plane where neutrons are generated'

    width = InvBase.d.float( name = 'width', default = 0.1, validator=InvBase.v.nonnegative)
    width.help = 'm, Width of rectangle in (x,y,0) plane where neutrons are generated'

    dist = InvBase.d.float( name = 'dist', default = 3, validator=InvBase.v.nonnegative)
    dist.help = 'm, Distance to target along z axis'

    xw = InvBase.d.float( name = 'xw', default = 0.1, validator=InvBase.v.nonnegative)
    xw.help = 'm, Width(x) of target'

    yh = InvBase.d.float( name = 'yh', default = 0.1, validator=InvBase.v.nonnegative)
    yh.help = 'm, Height(y) of target'

    E0 = InvBase.d.float( name = 'E0', default = 70., validator=InvBase.v.nonnegative)
    E0.help = 'meV, Mean energy of neutrons'

    dE = InvBase.d.float( name = 'dE', default = 50., validator=InvBase.v.nonnegative)
    dE.help = 'meV, Energy spread of neutrons (flat or gaussian sigma)'

    Lambda0 = InvBase.d.float( name = 'Lambda0', default = 0., validator=InvBase.v.nonnegative)
    Lambda0.help = 'AA, Mean wavelength of neutrons'

    dLambda = InvBase.d.float( name = 'dLambda', default = 0., validator=InvBase.v.nonnegative)
    dLambda.help = 'AA, Wavelength spread of neutrons'

    flux = InvBase.d.float( name = 'flux', default = 1, validator=InvBase.v.nonnegative)
    flux.help = '1/(s*cm**2*st), Energy integrated flux'

    gauss = InvBase.d.int( name = 'gauss', default = 0, validator=InvBase.v.nonnegative)
    gauss.help = 'Gaussian (1) or Flat (0) energy/wavelength distribution'


    dbtablename = 'simplesources'


SimpleSource.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
SimpleSourceTable = o2t(SimpleSource, {'subclassFrom': NeutronComponentTableBase})

__date__ = "$Mar 11, 2011 12:46:19 PM$"


