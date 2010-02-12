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


class UserHasRole(base):

    pyredbtablename = "user_has_roles"
    
    import dsaw.db
    
    id = dsaw.db.integer(name="id")
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    from User import User
    user = dsaw.db.reference(name='user', table=User)

    from Role import Role
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
    
    # get global pointer of user
    gp = user.globalpointer
    gp = gp and gp.id
    if not gp:
        msg = 'user %s is not referred yet. so it should not have a role' % user.id
        raise RuntimeError, msg

    # find the record
    where = "user='%s' and role='%s'" % (gp, role.id)
    try:
        r = db.query(UserHasRole).filter(where).one()
    except:
        msg = "Could no find user/role relation: user: %s, role: %s.\n" % (
            user, role)
        import traceback
        msg += 'traceback: %s' % traceback.format_exc()
        raise RuntimeError, msg
    
    #
    db.deleteRow(UserHasRole, where="id='%s'" % r.id)
    return


def inittable(db):
    associate('demo', ['roleU00002-demouser'], db, idgenerator=gid)
    associate('linjiao', ['roleD00001-coredeveloper'], db, idgenerator=gid)
    associate('jbrkeith', ['roleD00001-coredeveloper'], db, idgenerator=gid)
    associate('aivazis', ['roleR00001-internalreviewer'], db, idgenerator=gid)
    associate('btf', ['roleR00001-internalreviewer'], db, idgenerator=gid)
    associate('mmckerns', ['roleR00001-internalreviewer'], db, idgenerator=gid)
    return



# version
__id__ = "$Id$"

# End of file 
