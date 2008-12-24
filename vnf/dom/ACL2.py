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


def associate(user, roles, db, idgenerator=None):
    for role in roles:
        r = ACL2()
        r.id = idgenerator()
        r.user = user
        r.role = role
        db.insertRow(r)
        continue
    return

def inittable(db):
    associate(
        'role000001-demouser',
        ['roleCM0000-experimentsimulation', 'roleCM0001-bvk'],
        idgenerator=gid)
    associate('role000002-developer', 'superrole-all', idgenerator=gid)
    associate('role000001-internalreviewer', 'superrole-all', idgenerator=gid)
    return

# version
__id__ = "$Id$"

# End of file 
