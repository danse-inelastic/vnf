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

    energy = 70.
    
    pass


InvBase=base.Inventory
class Inventory(InvBase):

    energy = InvBase.d.float( name = 'energy', default = 70. )
    energy.tip = 'neutron energy. unit: meV'
    
    dbtablename = 'monochromaticsources'


MonochromaticSource.Inventory = Inventory
del Inventory


from _ import o2t
MonochromaticSourceTable = o2t(MonochromaticSource)


# version
__id__ = "$Id$"

# End of file 
