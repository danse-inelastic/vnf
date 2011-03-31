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


# test of acl. the acl-related table must have been initialzied by
#   bin/initdb.py --tables=users,roles,user_has_roles,privilege,role_has_privileges


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        import dsaw.db
        db = dsaw.db.connect(db='postgres:///vnfbeta')
        
        from vnfb.dom.User import User
        demo = db.query(User).filter_by(username='demo').one()
        
        from vnfb.utils.acl import hasPrivilege
        self.assert_(not hasPrivilege(demo, target='vasp', name='run', db=db))
        
        linjiao = db.query(User).filter_by(username='linjiao').one()
        
        from vnfb.utils.acl import hasPrivilege
        self.assert_(hasPrivilege(linjiao, target='bug', name='modify', db=db))
        
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
