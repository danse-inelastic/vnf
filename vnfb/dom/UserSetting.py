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


class UserSetting:

    show_help_on_login = True



from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    show_help_on_login = InvBase.d.bool(name='show_help_on_login', max_length = 128)
    dbtablename = 'usersettings'


UserSetting.Inventory = Inventory


from User import User
from dsaw.db.WithID import WithID
class TableBase(WithID):

    import dsaw.db

    user = dsaw.db.reference(name='user', table=User)

    pass # end of TableBase


from _ import o2t
UserSettingTable = o2t(UserSetting, {'subclassFrom': TableBase})


# version
__id__ = "$Id$"

# End of file 
