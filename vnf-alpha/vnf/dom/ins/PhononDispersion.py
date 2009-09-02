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


from registry import tableRegistry


from OwnedObject import OwnedObject as base1
from ComputationResult import ComputationResult as base2
class PhononDispersion(base1, base2):

    name = 'phonondispersions'

    import pyre.db
    matter = pyre.db.versatileReference(name='matter', tableRegistry=tableRegistry)

    datafiles = [
        'DOS',
        'Omega2',
        'Polarizations',
        'Qgridinfo',
        ]
    
    pass # end of Dispersion


def inittable(db):
    def new(id, creator='vnf'):
        r = PhononDispersion()
        r.id = id
        r.creator = creator
        return r

    records = [
        new('phonon-dispersion-fccNi-0'),
        ]

    for r in records: db.insertRow(r)
    return


def initids():
    return [
        'phonon-dispersion-fccNi-0',
        ]


# version
__id__ = "$Id$"

# End of file 
