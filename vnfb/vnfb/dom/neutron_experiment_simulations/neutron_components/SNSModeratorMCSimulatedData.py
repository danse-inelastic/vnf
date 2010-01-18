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


class SNSModeratorMCSimulatedData(object):

    instrument = ''
    short_description = ''

    pass



from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    instrument = InvBase.d.str(name='instrument')
    short_description = InvBase.d.str(name='short_description')

    dbtablename = 'snsmoderatormcsimulateddata'



SNSModeratorMCSimulatedData.Inventory = Inventory
del Inventory


from _ import o2t, NeutronComponentTableBase
SNSModeratorMCSimulatedDataTable = o2t(
    SNSModeratorMCSimulatedData, {'subclassFrom': NeutronComponentTableBase})

SNSModeratorMCSimulatedDataTable.datafiles = ['profile.dat']


# version
__id__ = "$Id$"

# End of file 
