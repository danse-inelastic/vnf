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


from AbstractNeutronComponent import AbstractNeutronComponent as base
class MonochromaticSource(base):

    abstract = False

    energy = 70.
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'energy',
            ]
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    energy = InvBase.d.float( name = 'energy', default = 70., validator=InvBase.v.positive)
    energy.help = 'neutron energy. unit: meV'
    
    dbtablename = 'monochromaticsources'


MonochromaticSource.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
MonochromaticSourceTable = o2t(MonochromaticSource, {'subclassFrom': NeutronComponentTableBase})


# version
__id__ = "$Id$"

# End of file 
