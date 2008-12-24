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


from Table import Table


class Role(Table):


    import pyre.db


    # the table name
    name = "roles"

    # the table columns
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = "PRIMARY KEY"

    rolename = pyre.db.varchar(name='id', length=64)

    description = pyre.db.varchar(name="description", length=255)
    status = pyre.db.char(name="status", length=1, default='l')
    # "l": live
    # "d": deleted


def inittable(db):
    def role(id, name, description):
        r = User()
        r.id = id
        r.rolename = name
        r.description = description
        return r
    records = [
        role('superrole-all', 'superuser', 'Super user who can do anything'),
        role('role000000-internalreviewer', 'internal-reviewer', 'Internal Reviewers of VNF'),
        role('role000001-demouser', 'demo-user', 'Demo user'),
        role('role000002-developer', 'developer', 'Developer'),
        role('roleCE0000-experimentsimulation', 'virtual-experimentalist', 'User of virtual experiments'),
        role('roleCM0000-vasp', 'vasp', 'VASP users'),
        role('roleCM0001-bvk-forward', 'bvk', 'BvK forward model users'),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'superrole-all',
        'role000000-internalreviewer',
        'role000001-demouser',
        'role000002-developer',
        'roleCE0000-experimentsimulation',
        'roleCM0000-vasp',
        'roleCM0001-bvk-forward',
        ]


# version
__id__ = "$Id$"

# End of file 
