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


class User(Table):

    name = "users"
    
    import pyre.db
    
    username = pyre.db.varchar(name="username", length=30)
    username.meta['tip'] = "the user's name"
    username.constraints = "PRIMARY KEY"
    
    password = pyre.db.varchar(name="password", length=30)
    password.meta['tip'] = "the user's password"

    fullname = pyre.db.varchar( name = 'fullname', length = 1024 )

    pass # end of User


def inittable(db):
    def user(name, pw, fullname):
        r = User()
        r.username = name
        r.password = pw
        r.fullname = fullname
        return r
    records = [
        user( 'demo', 'demo', 'demo user' ),
        ]
    for r in records: db.insertRow( r )
    return



# version
__id__ = "$Id$"

# End of file 
