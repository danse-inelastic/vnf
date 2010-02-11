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


from _ import Table


class Registrant(Table):


    import dsaw.db

    # the table name
    name = "registrants"

    # the table columns
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = "PRIMARY KEY"

    firstname = dsaw.db.varchar(name="firstname", length=16)
    lastname = dsaw.db.varchar(name="lastname", length=16)
    username = dsaw.db.varchar(name="username", length=64)
    password = dsaw.db.varchar(name="password", length=64)
    email = dsaw.db.varchar(name="email", length=256)
    
    organization = dsaw.db.varchar(name='organization', length=256)


# version
__id__ = "$Id$"

# End of file 
