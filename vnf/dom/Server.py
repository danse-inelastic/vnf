# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from dsaw.db.WithID import WithID as base
class Server(base):

    name = 'servers'

    import dsaw.db
    
    sname = dsaw.db.varchar( name='short_description', length = 128)
    sname.meta['tip'] = 'Server name'

    nodes    = dsaw.db.integer( name='nodes', default=1)
    nodes.meta['tip'] = 'Number of nodes on the server'

    corespernode = dsaw.db.integer( name='corespernode', default=1)
    corespernode.meta['tip'] = 'Number of cores per node. It is approximate, if it is different on nodes'

    short_description = dsaw.db.varchar( name='short_description', length = 128)
    short_description.meta['tip'] = 'short_description of server'

    address = dsaw.db.varchar(name='address', length = 128)
    address.meta['tip'] = 'address of server'

    port = dsaw.db.varchar(name='port', length = 8, default = '22')
    port.meta['tip'] = 'port of server'

    username = dsaw.db.varchar( name='username', length = 100)
    username.meta['tip'] = 'name of user that can run applications'

    workdir = dsaw.db.varchar( name='workdir', length = 1024)
    workdir.meta['tip'] = 'path in the server where jobs will be posted and run'

    #???
    group_access = dsaw.db.varchar(name='group_access', length = 128)
    group_access.meta['tip'] = 'which group of users has access to the server'
    
    #this should not be here. scheduler should be in the public interface of a "server"
    #we should build a wrapper service of schedulers and only connect to that service
    scheduler = dsaw.db.varchar( name='scheduler', length = 64)
    scheduler.meta['tip'] = 'scheduler to use on the server'

    status = dsaw.db.varchar(name='status', length=8, default='online')
    # online
    # offline


class LocalHost:

    address = None
    port = None




# version
__id__ = "$Id$"

# End of file 
