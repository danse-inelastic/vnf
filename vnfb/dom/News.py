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

    dbtablename = 'bvkbonds'


News.Inventory = Inventory


# version
__id__ = "$Id$"

# End of file 
