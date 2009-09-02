# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table as base
class Activity(base):

    name = 'activities'

    import dsaw.db

    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    username = dsaw.db.varchar(name='username', length=64)
    requesttime = dsaw.db.timestamp( name='requesttime' )
    actor = dsaw.db.varchar(name='actor', length=32)
    routine = dsaw.db.varchar(name='routine', length=128)

    remote_address = dsaw.db.varchar(name='remote_address', length=32)
    
    

# version
__id__ = "$Id$"

# End of file 
