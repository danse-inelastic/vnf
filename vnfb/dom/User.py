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


from _ import Table as base


class User(base):

    name = "users"
    
    import dsaw.db
    
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    username = dsaw.db.varchar(name="username", length=64)
    username.meta['tip'] = "the user's name"
    #username.constraints = "PRIMARY KEY"
    
    password = dsaw.db.varchar(name="password", length=64)
    password.meta['tip'] = "the user's password"

    fullname = dsaw.db.varchar(name='fullname', length=1024)

    email = dsaw.db.varchar(name='email', length=128)

    pass # end of User



# version
__id__ = "$Id$"

# End of file 
