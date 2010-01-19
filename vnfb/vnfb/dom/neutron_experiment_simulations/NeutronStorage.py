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

    description = ''
    
    pass


# orm
from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    description = InvBase.d.str(name='description', max_length=1024)

    dbtablename = 'neutronstorages'

NeutronStorage.Inventory = Inventory


# db table
from vnfb.dom.ComputationResult import ComputationResult
NeutronStorageTable = o2t(NeutronStorage, {'subclassFrom': ComputationResult})
NeutronStorageTable.datafiles = [
    'data.idf',
    ]



# version
__id__ = "$Id$"

# End of file 
