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
    
    roleid = pyre.db.varchar(name='roleid', length=64)
    roleid.constraints = 'REFERENCES roles (id)'
    
    pass # end of ACL2


def associate(userid, roleids, db, idgenerator=None):
    for roleid in roleids:
        r = ACL2()
        r.id = idgenerator()
        r.userid = userid
        r.roleid = roleid
        db.insertRow(r)
        continue
    return


def inittable(db):
    return


import random
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
def gid():
    prefix = 'acl1-'
    return prefix + ''.join(random.sample(alphabet, 32))


# version
__id__ = "$Id$"

# End of file 
