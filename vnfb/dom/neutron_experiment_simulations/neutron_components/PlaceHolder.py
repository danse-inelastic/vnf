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


# not a real component, just a place holder


from AbstractNeutronComponent import AbstractNeutronComponent as base
class PlaceHolder(base):

    abstract = False

    pass


InvBase=base.Inventory
class Inventory(InvBase):

    dbtablename = 'placeholdercomponents'


PlaceHolder.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase as TableBase
PlaceHolderTable = o2t(
    PlaceHolder, {'subclassFrom': TableBase})


# version
__id__ = "$Id$"

# End of file 
