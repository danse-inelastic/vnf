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


# role-role relation


from Table import Table as base


class ACL2(base):

    name = "acl2"
    
    import pyre.db
    
    id = pyre.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    userid = pyre.db.varchar(name='userid', length=64)
    userid.constraints = 'REFERENCES roles (id)'
    
    groupid = pyre.db.varchar(name='groupid', length=64)
    groupid.constraints = 'REFERENCES roles (id)'
    
    pass # end of ACL2


def associate(userid, groupids, db, idgenerator=None):
    for groupid in groupids:
        r = ACL2()
        r.id = idgenerator()
        r.userid = userid
        r.groupid = groupid
        db.insertRow(r)
        continue
    return


def inittable(db):
    return


import random
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
def gid():
    prefix = 'acl2-'
    return prefix + ''.join(random.sample(alphabet, 32))


# version
__id__ = "$Id$"

# End of file 
