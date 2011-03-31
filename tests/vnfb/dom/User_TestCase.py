#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


standalone = True

from vnf.dom.User import User
from vnf.dom.Role import Role
from vnf.dom.Privilege import Privilege
from vnf.dom.UserHasRole import UserHasRole
from vnf.dom.RoleHasRole import RoleHasRole
from vnf.dom.RoleHasPrivilege import RoleHasPrivilege, grant


import unittest
class TestCase(unittest.TestCase):

    def test(self):
        db = self.db

        linjiao = db.query(User).filter_by(id='linjiao').one()
        self.assert_(linjiao.hasRole(('vnf', 'admin'), db))
        self.assert_(linjiao.hasRole(('vnf', 'user'), db))

        demo = db.query(User).filter_by(id='demo').one()
        self.assert_(not demo.hasRole(('vnf', 'user'), db))
        self.assert_(demo.hasRole(('vnf', 'guest'), db))

        self.assert_(linjiao.hasPrivilege(('sample', 'write'), db))
        self.assert_(not demo.hasPrivilege(('sample', 'write'), db))
        return


    def setUp(self):
        import dsaw.db
        db = dsaw.db.connect(db='sqlite://')

        tables = [
            User, Role, Privilege,
            UserHasRole, RoleHasRole, RoleHasPrivilege,
            ]
        map(db.registerTable, tables)
        db.createAllTables()

        # users
        linjiao = User(); linjiao.id = linjiao.username = 'linjiao'
        db.insertRow(linjiao)

        demo = User(); demo.id = demo.username = 'demo'
        db.insertRow(demo)

        # roles
        vnfadmin = Role(); vnfadmin.rolename='admin'; vnfadmin.context='vnf'
        db.insertRow(vnfadmin)
        #
        vnfuser = Role(); vnfuser.rolename='user'; vnfuser.context='vnf'
        db.insertRow(vnfuser)
        #
        vnfguest = Role(); vnfguest.rolename='guest'; vnfguest.context='vnf'
        db.insertRow(vnfguest)

        # privileges
        writesample = Privilege(); writesample.name='write'; writesample.target='sample'
        db.insertRow(writesample)
        
        # linjiao is a vnf admin
        linjiao.assignRole(vnfadmin, db)

        # vnf admin can be vnf user
        vnfadmin.becomeMember(vnfuser, db)

        # demo is a guest
        demo.assignRole(vnfguest, db)

        # vnf user can write samples
        grant(writesample, vnfuser, db)

        self.db = db
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
