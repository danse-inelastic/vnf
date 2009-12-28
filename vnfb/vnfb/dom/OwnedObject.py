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


#from User import User

from dsaw.db.WithID import WithID
class OwnedObject(WithID):

    import dsaw.db

    creator = dsaw.db.varchar(name='creator', length=64)

    date = dsaw.db.date( name='date' )
    date.meta['tip'] = 'date of creation'

    short_description = dsaw.db.varchar(name='short_description', length = 128, default='')
    short_description.meta['tip'] = 'short_description'

    pass # end of OwnedObject


# version
__id__ = "$Id$"

# End of file 
