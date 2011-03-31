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
Test of component dom-access/material_simulations/phonons

Test assumes that
 1. database. see parameter "dbname"
 2. there is a phonons record in the db with data

'''

# phonons id.
phononsid = "bvk-fccAgAt293-N20-df0.2"



# application
from vnfb.testing.TestAppBase import Application as base
class TestApp(base):


    def main(self, testFacility, *args, **kwds):
        self.domaccess = self.retrieveDOMAccessor('material_simulations/phonons')
        testFacility.assert_(self.domaccess is not None)
        self.testFacility = testFacility
        
        self.test1()
        self.test2()
        return 


    def test1(self):
        domaccess = self.domaccess
        phonons = domaccess.getPhonons(phononsid)
        phonons = domaccess.getDataForPhonons(phonons)
        return


    def test2(self):
        domaccess = self.domaccess
        domaccess.standardizeDataInIDFFormat(phononsid)
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
