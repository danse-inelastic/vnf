# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import o2t

# data object
from vsat.Phonons import Phonons

# holder
from vnfb.dom.AtomicStructure import Structure, StructureTable

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name='matter', targettype=Structure, owned=0)

    short_description = InvBase.d.str(name='short_description')

    dbtablename = 'phonons'

Phonons.Inventory = Inventory
del Inventory


# db table
from ComputationResult import ComputationResult
#PhononDispersionTable = o2t(PhononDispersion, {'subclassFrom': ComputationResult})
PhononsTable = o2t(Phonons, {'subclassFrom': ComputationResult})
import dsaw.db
PhononsTable.addColumn(
    dsaw.db.reference(name='matter', table=StructureTable, backref='phonons')
    )

PhononsTable.datafiles = [
    'DOS',
    'Omega2',
    'Polarizations',
    'Qgridinfo',
    'WeightedQ', # this is optional actually
    ]


# version
__id__ = "$Id$"

# End of file 
