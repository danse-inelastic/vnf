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
 1. database. see parameter "dbname"

'''


from vnfb.testing import getDeploymentInfo
deploymentinfo = getDeploymentInfo()
dbname = deploymentinfo.dbname


#
import os
dataroot = deploymentinfo.dataroot


# application
from luban.applications.UIApp import UIApp as base
class TestApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory


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


    def _getPrivateDepositoryLocations(self):
        return deploymentinfo.pyre_depositories


    def _configure(self):
        # db
        self.inventory.clerk.inventory.db = dbname
        self.inventory.clerk._configure()
        #
        super(TestApp, self)._configure()

        # guid.dat
        self.inventory.guid.datastore_path = deploymentinfo.guid_datastore_path
        return


    def _init(self):
        #
        super(TestApp, self)._init()
        # data root
        self.dds.dataroot = dataroot
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
