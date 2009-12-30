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

    pass



from vnfb.dom.neutron_experiment_simulations.Instrument import Instrument

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    instrument = InvBase.d.str(name='instrument')

    dbtablename = 'snsmoderatormcsimulateddata'



SNSModeratorMCSimulatedData.Inventory = Inventory
del Inventory


from _ import o2t
SNSModeratorMCSimulatedDataTable = o2t(SNSModeratorMCSimulatedData)

SNSModeratorMCSimulatedDataTable.datafiles = ['profile.dat']


# obsolete...
def inittable(db):

    def data(id, instrument):
        r = SNSModeratorMCSimulatedData()
        r.id = id
        r.instrument = instrument
        return r
    records = [
        data('sct521_bu_17_1-ARCS', 'ARCS'),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'sct521_bu_17_1-ARCS',
        ]


# version
__id__ = "$Id$"

# End of file 
