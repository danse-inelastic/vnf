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

    rolename = pyre.db.varchar(name='rolename', length=64)

    description = pyre.db.varchar(name="description", length=255)
    status = pyre.db.char(name="status", length=1, default='l')
    # "l": live
    # "d": deleted


def inittable(db):
    def role(id, name, description):
        r = Role()
        r.id = id
        r.rolename = name
        r.description = description
        return r
    records = [
        role('role000000-administrator', 'administrator', 'Administrator'),
        role('roleD00001-coredeveloper', 'core-developer', 'Core Developer'),
        role('roleD00002-developer', 'developer', 'Developer'),
        role('roleR00001-internalreviewer', 'internal-reviewer', 'Internal Reviewers of VNF'),
        role('roleU00001-user', 'user', 'User'),
        role('roleU00002-demouser', 'demo-user', 'Demo user'),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'role000000-administrator',
        'roleD00001-coredeveloper',
        'roleD00002-developer',
        'roleR00001-internalreviewer',
        'roleU00001-user',
        'roleU00002-demouser',
        ]


# version
__id__ = "$Id$"

# End of file 
