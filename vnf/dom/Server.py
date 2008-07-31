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


from Table import Table
class Server(Table):

    name = 'servers'

    import pyre.db
    
    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    server = pyre.db.varchar(name='server', length = 128)
    server.meta['tip'] = 'name of server'

    location = pyre.db.varchar( name='location', length = 128)
    location.meta['tip'] = 'location of server'

    groupAccess = pyre.db.varchar(name='groupAccess', length = 128)
    groupAccess.meta['tip'] = 'which group of users has access to the server'
    
    username = pyre.db.varchar( name='username', length = 100)
    username.meta['tip'] = 'name of user that can run applications'

    workdir = pyre.db.varchar( name='workdir', length = 1024)
    workdir.meta['tip'] = 'path in the server where jobs will be posted and run'

    scheduler = pyre.db.varchar( name='scheduler', length = 64)
    scheduler.meta['tip'] = 'scheduler to use on the server'



# version
__id__ = "$Id$"

# End of file 
