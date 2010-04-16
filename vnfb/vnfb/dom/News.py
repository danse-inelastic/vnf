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


class News:

    title = ''
    content = ''



from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    title = InvBase.d.str(name='title', max_length = 128)
    content = InvBase.d.str(name='content', max_length = 65536)
    
    dbtablename = 'news'


News.Inventory = Inventory


from dsaw.db.WithID import WithID
class TableBase(WithID):

    import dsaw.db

    creator = dsaw.db.varchar(name='creator', length=64)

    time = dsaw.db.timestamp( name='time' )
    time.meta['tip'] = 'time of creation'

    pass # end of TableBase


from _ import o2t
NewsTable = o2t(News, {'subclassFrom': TableBase})


# version
__id__ = "$Id$"

# End of file 
