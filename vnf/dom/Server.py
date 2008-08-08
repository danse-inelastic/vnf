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

    hostname = pyre.db.varchar(name='hostname', length = 128)
    hostname.meta['tip'] = 'hostname of server'

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


def initialization_records():
    def server(id, hostname, location, groupAccess, username, workdir, scheduler):
        r = Server()
        r.id = id
        r.hostname = hostname
        r.location = location
        r.groupAccess = groupAccess
        r.username = username
        r.workdir = workdir
        r.scheduler = scheduler
        return r
    return [
        server( 'server0', '127.0.0.1', 'local',
                'local users', 'vnf', '/home/vnf/jobs', 'torque' ),
        ]

# version
__id__ = "$Id$"

# End of file 
