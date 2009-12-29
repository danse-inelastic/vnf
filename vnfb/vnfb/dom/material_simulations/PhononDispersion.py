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
class PhononDispersion(object):

    matter = None


# orm
from vnfb.dom.AtomicStructure import Structure

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name='matter', targettype=None, targettypes=[Structure], owned=0)

    dbtablename = 'phonondispersions'

PhononDispersion.Inventory = Inventory
del Inventory


# db table
from ComputationResult import ComputationResult
PhononDispersionTable = o2t(PhononDispersion, {'subclassFrom': ComputationResult})
PhononDispersionTable.datafiles = [
    'DOS',
    'Omega2',
    'Polarizations',
    'Qgridinfo',
    ]



# version
__id__ = "$Id$"

# End of file 
