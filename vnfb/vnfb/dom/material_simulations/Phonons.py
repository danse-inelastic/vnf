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

from vnfb.dom.AtomicStructure import StructureTable
# vnf holder
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
