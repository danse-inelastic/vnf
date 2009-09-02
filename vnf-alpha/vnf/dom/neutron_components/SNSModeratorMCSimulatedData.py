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


from dsaw.db.Table import Table

class SNSModeratorMCSimulatedData(Table):

    name = 'snsmoderatormcsimulateddata'

    import dsaw.db

    id = dsaw.db.varchar(name='id', length=128, default='')
    instrument = dsaw.db.varchar(name='instrument', length=32, default='')

    datafiles = ['profile.dat']

    pass # end of SNSModerator


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
