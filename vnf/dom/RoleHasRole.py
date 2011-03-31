# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2008-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# role-role relation


from _ import Table as base
from Role import Role


class RoleHasRole(base):

    pyredbtablename = "role_has_roles"
    
    import dsaw.db
    
    id = dsaw.db.integer(name="id")
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    member = dsaw.db.reference(name='member', table=Role)
    group = dsaw.db.reference(name='group', table=Role)
    
    pass # end of RoleHasRole


def join(member, group, db):
    'make the give role (member) as a member of the given group'
    r = RoleHasRole()
    r.group = group
    r.member = member
    db.insertRow(r)
    return


def leave(member, group, db):
    'make the member leave from the given group'
    # find the record
    try:
        r = db.query(RoleHasRole).filter_by(group=group.id, member=member.id).one()
    except:
        msg = "Could no find role/role relation: group: %s, member: %s.\n" % (
            group, member)
        import traceback
        msg += 'traceback: %s' % traceback.format_exc()
        raise RuntimeError, msg
    
    #
    db.deleteRow(RoleHasRole, where="id='%s'" % r.id)
    return


# version
__id__ = "$Id$"

# End of file 
