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


# Methods about access control list

def containsRole(role1, role2, db):
    'check if role1 contains role2'
    
    # super user can act as any role
    if role1.id == 'superuser': return True
    
    ACL = _acls.get(role1.__class__)
    if ACL is None: raise RuntimeError, "cannot find access control list for %s, %s" % (
        role1.__class__.__name__, role1.id)
    where = "user='%s' and role='%s'" % (role1.id, role2.id)
    if db.fetchall(ACL, where=where): return True
    else:
        myroles = _findRoles(role1, db)
        for myrole in myroles:
            if containsRole(myrole, role2): return True
            continue
    return False


def _findRoles(role, db):
    ACL = _acls.get(role.__class__)
    where = "user='%s'" % role.id
    return db.fetchall(ACL, where=where)


from ACL1 import ACL1
from ACL2 import ACL2
_acls = {
    User: ACL1,
    Role: ACL2,
    }


# version
__id__ = "$Id$"

# End of file 
