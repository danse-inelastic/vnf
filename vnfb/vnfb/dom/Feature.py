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


class Feature:

    description = ''
    status = ''
    developer = '' # developer who is responsible for this feature



from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    description = InvBase.d.str(name='description', max_length = 256)
    status = InvBase.d.str(name='status', max_length = 16)
    developer = InvBase.d.str(name='developer', max_length = 64)
    
    dbtablename = 'features'


Feature.Inventory = Inventory


from dsaw.db.WithID import WithID
class TableBase(WithID):

    import dsaw.db

    pass # end of TableBase


from _ import o2t
FeatureTable = o2t(Feature, {'subclassFrom': TableBase})


# version
__id__ = "$Id$"

# End of file 
