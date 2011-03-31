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


# user-role relation


from _ import Table as base
from User import User
from Role import Role


class UserHasRole(base):

    pyredbtablename = "user_has_roles"
    
    import dsaw.db
    
    id = dsaw.db.integer(name="id")
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    user = dsaw.db.reference(name='user', table=User)

    role = dsaw.db.reference(name='role', table=Role)
    
    pass # end of UserHasRole


def assign(role, user, db):
    'assign a role to a user'
    r = UserHasRole()
    r.user = user
    r.role = role
    db.insertRow(r)
    return


def remove(role, user, db):
    'remove a role from a user'
    # find the record
    try:
        r = db.query(UserHasRole).filter_by(user=user.id, role=role.id).one()
    except:
        msg = "Could no find user/role relation: user: %s, role: %s.\n" % (
            user, role)
        import traceback
        msg += 'traceback: %s' % traceback.format_exc()
        raise RuntimeError, msg
    
    #
    db.deleteRow(UserHasRole, where="id='%s'" % r.id)
    return


# version
__id__ = "$Id$"

# End of file 
