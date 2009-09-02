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


from Table import Table as base


class ACL1(base):

    name = "acl1"
    
    import dsaw.db
    
    id = dsaw.db.varchar(name="id", length=64)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    userid = dsaw.db.varchar(name='userid', length=64)
    userid.constraints = 'REFERENCES users (id)'
    
    groupid = dsaw.db.varchar(name='groupid', length=64)
    groupid.constraints = 'REFERENCES roles (id)'
    
    pass # end of ACL1


def associate(userid, groupids, db, idgenerator=None):
    for groupid in groupids:
        r = ACL1()
        r.id = idgenerator()
        r.userid = userid
        r.groupid = groupid
        db.insertRow(r)
        continue
    return


def deassociate(userid, groupids, db):
    where = "userid='%s'" % userid
    all = db.fetchall(ACL1, where=where)
    for r in all:
        if r.groupid in groupids:
            db.deleteRow(ACL1, where="id='%s'" % r.id)
        continue
    return


def inittable(db):
    associate('demo', ['roleU00002-demouser'], db, idgenerator=gid)
    associate('linjiao', ['roleD00001-coredeveloper'], db, idgenerator=gid)
    associate('jbrkeith', ['roleD00001-coredeveloper'], db, idgenerator=gid)
    associate('aivazis', ['roleR00001-internalreviewer'], db, idgenerator=gid)
    associate('btf', ['roleR00001-internalreviewer'], db, idgenerator=gid)
    associate('mmckerns', ['roleR00001-internalreviewer'], db, idgenerator=gid)
    return


def cleartable(db):
    deassociate('demo', ['roleU00002-demouser'], db)
    deassociate('linjiao', ['roleD00001-coredeveloper'], db)
    deassociate('jbrkeith', ['roleD00001-coredeveloper'], db)
    deassociate('aivazis', ['roleR00001-internalreviewer'], db)
    deassociate('btf', ['roleR00001-internalreviewer'], db)
    deassociate('mmckerns', ['roleR00001-internalreviewer'], db)
    return


import random
alphabet = "0123456789abcdefghijklmnopqrstuvwxyz"
def gid():
    prefix = 'acl1-'
    return prefix + ''.join(random.sample(alphabet, 32))


# version
__id__ = "$Id$"

# End of file 
