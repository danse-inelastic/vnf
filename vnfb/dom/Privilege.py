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


class Privilege(Table):
    
    
    import dsaw.db
    
    
    # the table name
    pyredbtablename = "privileges"
    
    # the table columns
    id = dsaw.db.integer(name="id")
    id.constraints = "PRIMARY KEY"

    # target of the privilege. think of unix file system, target is like the diretory or file
    target = dsaw.db.varchar(name='target', length=64)
    
    # name of the privilege. think of unix file system, name is sth like 'r', 'w', 'x'
    name = dsaw.db.varchar(name='name', length=64)

    #
    description = dsaw.db.varchar(name="description", length=255)
    


# version
__id__ = "$Id$"

# End of file 
