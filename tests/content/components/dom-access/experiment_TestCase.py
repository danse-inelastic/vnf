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


'''
Test of component dom-access/experiment

Test assumes that
 1. database. the dbname variable of the current deployment

'''


# application
from vnfb.testing.TestAppBase import Application as base
class TestApp(base):


    def main(self, testFacility, *args, **kwds):
        self.domaccess = self.retrieveDOMAccessor('experiment')
        testFacility.assert_(self.domaccess is not None)
        self.testFacility = testFacility
        
        self.test1()
        return 


    def test1(self):
        tf = self.testFacility
        domaccess = self.domaccess
        self.sentry.username = 'linjiao'
        exp = domaccess.createExperiment()
        tf.assertEqual(domaccess.orm(exp).creator, self.sentry.username)
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
