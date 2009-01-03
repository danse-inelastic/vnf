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


# version
__id__ = "$Id: Registrant.py,v 1.1 2008-04-04 06:39:23 aivazis Exp $"

# End of file 
