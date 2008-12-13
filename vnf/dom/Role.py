#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                             Michael A.G. Aivazis
#                               Orthologue, Ltd.
#                      (C) 2004-2006  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table


class Role(Table):


    import pyre.db


    # the table name
    name = "roles"

    # the table columns
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = "PRIMARY KEY"

    description = pyre.db.varchar(name="description", length=255)
    status = pyre.db.char(name="status", length=1)


# version
__id__ = "$Id$"

# End of file 
