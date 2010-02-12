#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from _ import Table


class Role(Table):
    
    
    import dsaw.db
    
    
    # the table name
    name = "roles"
    
    # the table columns
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = "PRIMARY KEY"

    # name of the role, like "admin", "user", "developer"
    rolename = dsaw.db.varchar(name='rolename', length=64)
    
    # context of the role, like "mcvine", "vasp", "vnf"
    context = dsaw.db.varchar(name='context', length=64)
    
    description = dsaw.db.varchar(name="description", length=255)
    status = dsaw.db.char(name="status", length=1, default='l')
    # "l": live
    # "d": deleted


# version
__id__ = "$Id$"

# End of file 
