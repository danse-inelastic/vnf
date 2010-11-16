# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


#from User import User

from dsaw.db.WithID import WithID
class OwnedObjectTs(WithID):

    import dsaw.db

    creator = dsaw.db.varchar(name='creator', length=64)

    timestamp = dsaw.db.timestamp( name='timestamp' )
    timestamp.meta['tip'] = 'timestamp of creation'


# version
__id__ = "$Id$"

# End of file 
