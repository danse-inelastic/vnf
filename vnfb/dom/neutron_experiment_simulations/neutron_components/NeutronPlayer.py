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
class NeutronPlayer(base):

    neutrons = None
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            ]
        drawer.sequence = ['properties', 'neutrons']
    pass



from vnfb.dom.neutron_experiment_simulations.NeutronStorage import NeutronStorage

InvBase=base.Inventory
class Inventory(InvBase):

    neutrons = InvBase.d.reference(name='neutrons', targettype=NeutronStorage, owned=False)
    dbtablename = 'neutronplayers'



NeutronPlayer.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase as TableBase
NeutronPlayerTable = o2t(NeutronPlayer, {'subclassFrom':TableBase})


# version
__id__ = "$Id$"

# End of file 
