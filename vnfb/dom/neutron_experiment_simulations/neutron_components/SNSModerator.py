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

    neutronprofile = None
    width = height = 0.1
    dist = 2.5
    xw = yh = 0.1
    Emin = 0; Emax = 100
    
    pass


from SNSModeratorMCSimulatedData import SNSModeratorMCSimulatedData
InvBase=base.Inventory
class Inventory(InvBase):
    
    width = InvBase.d.float(name='width', default=0.1)
    height = InvBase.d.float(name='height', default=0.1)
    dist = InvBase.d.float(name='dist', default=2.5)
    xw = InvBase.d.float(name='xw', default=0.1)
    yh = InvBase.d.float(name='yh', default=0.1)
    Emin = InvBase.d.float(name='Emin', default=0)
    Emax = InvBase.d.float(name='Emax', default=100)
    neutronprofile = InvBase.d.reference(name='neutronprofile', targettype=SNSModeratorMCSimulatedData)

    dbtablename = 'snsmoderators'


SNSModerator.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
SNSModeratorTable = o2t(SNSModerator, {'subclassFrom': NeutronComponentTableBase})


# version
__id__ = "$Id$"

# End of file 
