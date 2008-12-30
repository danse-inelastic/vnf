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


def registerPrivilegeCheckingHandler(type, handler):
    global _privilege_checking_handlers
    _privilege_checking_handlers[type]=handler
    return


def checkPrivilege(role, privilege, db):
    'check if role has privilege'
    # check if it is a role or a user
    if isinstance(role, Role):
        # for a role, check if it has direct privilege
        handler = _getPrivilegeCheckingHandler(privilege.__class__)
        # if yes, we are good
        if handler(role.id, privilege.id, db): return True

    # get all roles that this role can assume
    myroles = _findRoles(role, db)

    # loop over all those roles and find out if they have the
    # requested privilege
    for myrole in myroles:
        if checkPrivilege(myrole, privilege, db): return True
        continue

    # nothing found, no privilege
    return False


from User import User
from Role import Role
from ACL1 import ACL1
from ACL2 import ACL2
_roleacls = {
    User: ACL1,
    Role: ACL2,
    }
def _findRoles(role, db):
    RoleACL = _roleacls.get(role.__class__)
    if RoleACL is None: raise RuntimeError, "cannot find access control list for %s, %s" % (
        role.__class__.__name__, role.id)
    where = "userid='%s'" % role.id
    def getRole(id): return db.fetchall(Role, where="id='%s'" % id)[0]
    return [getRole(acl.groupid) for acl in db.fetchall(RoleACL, where=where)]


_privilege_checking_handlers = {}
def _getPrivilegeCheckingHandler(type):
    h = _privilege_checking_handlers.get(type)
    if h is None:
        raise RuntimeError, "privilege checking handler for type %s is not defined" % (type.__name__)
    return h


# version
__id__ = "$Id$"

# End of file 
