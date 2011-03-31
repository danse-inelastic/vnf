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
class SNSModerator(base):

    abstract = False

    neutronprofile = None
    width = height = 0.1
    dist = 2.5
    xw = yh = 0.1
    Emin = 0; Emax = 100
    
    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = ['properties', 'neutronprofile']
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'width', 'height',
            'dist',
            'xw', 'yh',
            'Emin', 'Emax',
            ]

    pass


from SNSModeratorMCSimulatedData import SNSModeratorMCSimulatedData
InvBase=base.Inventory
class Inventory(InvBase):
    
    width = InvBase.d.float(name='width', default=0.1)
    width.tip = "width of the moderator. unit: meter"

    height = InvBase.d.float(name='height', default=0.1)
    height.tip = "height of the moderator. unit: meter"

    dist = InvBase.d.float(name='dist', default=2.5)
    dist.tip = "distance from moderator to its target. unit: meter"

    xw = InvBase.d.float(name='xw', default=0.1)
    xw.tip = "x (horizontal) dimension of the target. unit: meter"

    yh = InvBase.d.float(name='yh', default=0.1)
    yh.tip = "y (vertical) dimension of the target. unit: meter"
    
    Emin = InvBase.d.float(name='Emin', default=0)
    Emin.tip = 'minimum value for energy of neutrons. unit: meV'

    Emax = InvBase.d.float(name='Emax', default=100)
    Emax.tip = 'maximum value for energy of neutrons. unit: meV'

    neutronprofile = InvBase.d.reference(
        name='neutronprofile', targettype=SNSModeratorMCSimulatedData, owned=False)
    neutronprofile.tip = 'Select a neutron profile for the instrument in which you want to run your experiment'

    dbtablename = 'snsmoderators'


SNSModerator.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
SNSModeratorTable = o2t(SNSModerator, {'subclassFrom': NeutronComponentTableBase})


# version
__id__ = "$Id$"

# End of file 
