#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# application
from vnf.testing.TestAppBase import Application as base
class TestApp(base):


    def main(self, testFacility, *args, **kwds):
        super(TestApp, self).main(testFacility)
        self.test1()
        return 


    def test1(self):
        tf = self.testFacility
        
        db = self.clerk.db
        
        from vnf.dom.User import User
        demo = db.query(User).filter_by(username='demo').one()
        
        from vnf.utils.acl import hasPrivilege
        tf.assert_(not hasPrivilege(demo, target='vasp', name='run', db=db))
        
        linjiao = db.query(User).filter_by(username='linjiao').one()
        
        from vnf.utils.acl import hasPrivilege
        tf.assert_(hasPrivilege(linjiao, target='bug', name='modify', db=db))
        return


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        app = TestApp('main')
        app.run(self)
        return


def main():
    unittest.main()
    return

if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
