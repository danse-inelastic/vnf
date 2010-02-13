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

# test of User table. the user-related table must have been initialzied by
#   bin/initdb.py --tables=users,roles,user_has_roles


import unittest
class TestCase(unittest.TestCase):

    def test(self):
        import dsaw.db
        db = dsaw.db.connect(db='postgres:///vnfbeta')
        
        from vnfb.dom.User import User
        user = db.query(User).filter_by(username='demo').one()

        self.assert_(user.hasRole(('vnf', 'guest'), db))
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
