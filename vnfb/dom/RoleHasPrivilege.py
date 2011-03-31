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


# role-privilege relation


from _ import Table as base
from Role import Role
from Privilege import Privilege


class RoleHasPrivilege(base):

    pyredbtablename = "role_has_privileges"
    
    import dsaw.db
    
    id = dsaw.db.integer(name="id")
    id.constraints = 'PRIMARY KEY'

    role = dsaw.db.reference(name='role', table=Role)
    
    privilege = dsaw.db.reference(name='privilege', table=Privilege)

    pass # end of RoleHasPrivilege


def grant(privilege, role, db):
    'grant a privilege to a role'
    r = RoleHasPrivilege()
    r.privilege = privilege
    r.role = role
    db.insertRow(r)
    return


def revoke(privilege, role, db):
    'revoke a privilege assigment from a role'
    
    try:
        r = db.query(RoleHasPrivilege).filter_by(role=role.id, privilege=privilege.id).one()
    except:
        msg = "Could no find role/privilege relation: role: %s, privilege: %s.\n" % (
            role, privilege)
        import traceback
        msg += 'traceback: %s' % traceback.format_exc()
        raise RuntimeError, msg
    
    #
    db.deleteRow(RoleHasPrivilege, where="id='%s'" % r.id)
    return


# version
__id__ = "$Id$"

# End of file 
