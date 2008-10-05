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


from Table import Table as base


class User(base):

    name = "users"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=100)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    username = pyre.db.varchar(name="username", length=30)
    username.meta['tip'] = "the user's name"
    #username.constraints = "PRIMARY KEY"
    
    password = pyre.db.varchar(name="password", length=30)
    password.meta['tip'] = "the user's password"

    fullname = pyre.db.varchar(name='fullname', length=1024)

    email = pyre.db.varchar(name='email', length=128)

    pass # end of User


def inittable(db):
    def user(name, pw, fullname, email):
        r = User()
        r.id = name
        r.username = name
        r.password = pw
        r.fullname = fullname
        r.email = email
        return r
    records = [
        user( 'demo', 'demo', 'demo user', 'vnfdemo@hotmail.com' ),
        ]
    for r in records: db.insertRow( r )
    return



# version
__id__ = "$Id$"

# End of file 
