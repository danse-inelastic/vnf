# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Table import Table as base


class ACL2(base):

    name = "acl2"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    user = pyre.db.varchar(name='user', length=64)
    user.constraints = 'REFERENCES roles (id)'
    
    role = pyre.db.varchar(name='role', length=64)
    role.constraints = 'REFERENCES roles (id)'
    
    pass # end of ACL2


def inittable(db):
    return


def initids():
    return []


# version
__id__ = "$Id$"

# End of file 
