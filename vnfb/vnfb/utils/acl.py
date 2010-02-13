# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def hasPrivilege(user, target=None, name=None, db=None):
    '''check if the user has the given privilege

    user: db record in users table
    target: target of the privilege. see Privilege class for more details
    name: name of the privilege. see Privilege class for more details
    db: db connection
    '''
    return _hasPrivilege(user, (target,name), db)


def _hasPrivilege(user, privilege, db):
    '''check if the user has the given privilege

    user: db record in users table
    privilege: either of following two
      1. a tuple of (target, name)
      2. a record in the privileges table
      
    '''
    # the implementation here first find all the roles that
    # has the given privilege, then test if the user has
    # one of the roles.

    # in the future, when role_has_roles is created, we
    # need a recursion algorithm

    if isinstance(privilege, tuple):
        target, name = privilege
        from vnfb.dom.Privilege import Privilege
        privilege = db.query(Privilege).filter_by(target=target, name=name).one()

    roles = privilege.findRoles(db)
    
    for role in roles:
        if user.hasRole(role, db): return True
        continue
    return False


# version
__id__ = "$Id$"

# End of file 
