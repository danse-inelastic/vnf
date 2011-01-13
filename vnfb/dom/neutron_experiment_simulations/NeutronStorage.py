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
# each instance represents a data storage in which simulated neutrons are stored
class NeutronStorage:

    short_description = ''

    def __str__(self):
        return 'Neutron storage(%s)' % self.short_description
    
    pass


# orm
from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    short_description = InvBase.d.str(name='short_description')

    dbtablename = 'neutronstorages'

NeutronStorage.Inventory = Inventory


# db table
from vnfb.dom.ComputationResult import ComputationResult
NeutronStorageTable = o2t(NeutronStorage, {'subclassFrom': ComputationResult})
NeutronStorageTable.datafiles = [
    'data.idf',
    ]
NeutronStorageTable.short_description.length = 1024



# version
__id__ = "$Id$"

# End of file 
