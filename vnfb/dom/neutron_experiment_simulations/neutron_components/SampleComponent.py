# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from AbstractNeutronComponent import AbstractNeutronComponent as base

# this is the "place-holder" sample component to be used in neutron instrument
class SampleComponent(base):

    abstract = False

    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'referencename', 'position', 'orientation',
            ]

    pass # end of SampleComponent


class Inventory(base.Inventory):

    dbtablename = 'samplecomponents'
    pass

SampleComponent.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
SampleComponentTable = o2t(
    SampleComponent,
    {'subclassFrom': NeutronComponentTableBase},
    )


# version
__id__ = "$Id$"

# End of file 
