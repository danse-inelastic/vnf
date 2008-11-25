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


from pyre.db.Table import Table

class SNSModeratorMCSimulatedData(Table):

    name = 'snsmoderatormcsimulateddata'

    import pyre.db

    id = pyre.db.varchar(name='id', length=128, default='')
    instrument = pyre.db.varchar(name='instrument', length=32, default='')

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


# version
__id__ = "$Id$"

# End of file 
