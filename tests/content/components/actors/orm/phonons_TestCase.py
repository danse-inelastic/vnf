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
Test of component actors/orm/phonons

Test assumes that
 1. there is a phonons record in the db with data

'''

# phonons id.
phononsid = "bvk-fccAgAt293-N20-df0.2"
# phononsid = "8VDEZDF"


# application
from vnf.testing.TestAppBase import Application as base
class TestApp(base):


    def main(self, testFacility, *args, **kwds):
        self.actor = self.retrieveActor('orm/phonons')
        self.actor.inventory.id = phononsid
        
        testFacility.assert_(self.actor is not None)
        self.testFacility = testFacility

        self.chroot()
        self.test1()
        self.test2()
        return 


    def test1(self):
        actor = self.actor
        phonons = actor._load(self)
        print actor._createPlotAndDataLink(phonons, self)
        return


    def test2(self):
        actor = self.actor
        actor.createGraphicalView(self)
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
