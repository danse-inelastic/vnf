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
        user( 'demo', 'fe01ce2a7fbac8fafaed7c982a04e229', 'demo user', 'vnfdemo@hotmail.com' ),
        user( '__method__', 'md5', 'not a real user', '' ),
        user( 'linjiao', '8cdd1ccd7f5a14d3e70c1fd0bb0b7198', 'Jiao Lin', 'linjiao@caltech.edu' ),
        user( 'jbrkeith', '1015488bc40a5eedfd0795d4bd399973', 'J Brandon Keith', 'jbrkeith@caltech.edu' ),
        user( 'aivazis', '1015488bc40a5eedfd0795d4bd399973', 'Michael Aivazis', 'aivazis@caltech.edu' ),
        user( 'btf', '1015488bc40a5eedfd0795d4bd399973', 'Brent Fultz', 'btf@caltech.edu' ),
        user( 'mmckerns', '1015488bc40a5eedfd0795d4bd399973', 'Michael Mckerns', 'mmckerns@caltech.edu' ),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        '__method__',
        'demo',
        'linjiao',
        'jbrkeith',
        'aivazis',
        'btf',
        'mmckerns',
        ]

# version
__id__ = "$Id$"

# End of file 
