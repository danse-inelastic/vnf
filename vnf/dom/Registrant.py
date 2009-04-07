#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table


class Registrant(Table):


    import pyre.db

    # the table name
    name = "registrants"

    # the table columns
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = "PRIMARY KEY"

    firstname = pyre.db.varchar(name="firstname", length=16)
    lastname = pyre.db.varchar(name="lastname", length=16)
    username = pyre.db.varchar(name="username", length=64)
    password = pyre.db.varchar(name="password", length=64)
    email = pyre.db.varchar(name="email", length=256)
    
    organization = pyre.db.varchar(name='organization', length=256)


def inittable(db):
    def registrant(firstname, lastname, username, pw, email, organization):
        r = Registrant()
        r.firstname = firstname
        r.lastname = lastname
        r.id = username
        r.username = username
        r.password = pw
        r.email = email
        r.organization = organization
        return r
    records = [
        registrant( 'Jiao', 'Lin', 'linjiao', '8cdd1ccd7f5a14d3e70c1fd0bb0b7198', 'linjiao@caltech.edu', 'Caltech'),
        registrant( 'J Brandon', 'Keith', 'jbrkeith', '1015488bc40a5eedfd0795d4bd399973', 'jbrkeith@caltech.edu', 'Caltech' ),
        registrant( 'Michael', 'Aivazis', 'aivazis', '1015488bc40a5eedfd0795d4bd399973',  'aivazis@caltech.edu', 'Caltech' ),
        registrant( 'Brent', 'Fultz', 'btf', '1015488bc40a5eedfd0795d4bd399973', 'btf@caltech.edu', 'Caltech' ),
        registrant( 'Michael', 'Mckerns', 'mmckerns', '1015488bc40a5eedfd0795d4bd399973', 'mmckerns@caltech.edu', 'Caltech' ),
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
__id__ = "$Id: Registrant.py,v 1.1 2008-04-04 06:39:23 aivazis Exp $"

# End of file 
