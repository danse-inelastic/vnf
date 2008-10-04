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

    short_description = pyre.db.varchar( name='short_description', length = 128)
    short_description.meta['tip'] = 'short_description of server'

    address = pyre.db.varchar(name='address', length = 128)
    address.meta['tip'] = 'address of server'

    port = pyre.db.varchar(name='port', length = 8, default = '22')
    port.meta['tip'] = 'port of server'

    username = pyre.db.varchar( name='username', length = 100)
    username.meta['tip'] = 'name of user that can run applications'

    workdir = pyre.db.varchar( name='workdir', length = 1024)
    workdir.meta['tip'] = 'path in the server where jobs will be posted and run'

    #???
    group_access = pyre.db.varchar(name='group_access', length = 128)
    group_access.meta['tip'] = 'which group of users has access to the server'
    
    #this should not be here. scheduler should be in the public interface of a "server"
    #we should build a wrapper service of schedulers and only connect to that service
    scheduler = pyre.db.varchar( name='scheduler', length = 64)
    scheduler.meta['tip'] = 'scheduler to use on the server'


def inittable(db):
    def server(
        id, short_description,
        address, port,
        username, workdir,
        group_access,
        scheduler):
        
        r = Server()
        r.id = id
        r.short_description = short_description
        r.address = address
        r.port = port
        r.username = username
        r.workdir = workdir
        r.group_access = group_access
        r.scheduler = scheduler
        return r

    records = [
        server(
        'server000', 'default server (octopod)',
        'localhost', '54321',
        'linjiao', '/home/linjiao/vnfjobs', 
        'group access???',
        'torque',
        ),
        ]
    for r in records: db.insertRow( r )
    return

# version
__id__ = "$Id$"

# End of file 
