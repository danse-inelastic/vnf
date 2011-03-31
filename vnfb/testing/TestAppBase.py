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
This provides a base class for test application.

XXX:
This could be merged with the main application of vnf.

'''


from vnf.testing import getDeploymentInfo
deploymentinfo = getDeploymentInfo()


# application
from luban.applications.UIApp import UIApp as base
class Application(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, testFacility, *args, **kwds):
        self.testFacility = testFacility
        return 


    def _getPrivateDepositoryLocations(self):
        return deploymentinfo.pyre_depositories


    def _configure(self):
        # db
        self.inventory.clerk.inventory.db = deploymentinfo.dbname
        self.inventory.clerk._configure()
        #
        super(Application, self)._configure()

        # guid.dat
        self.inventory.guid.datastore_path = deploymentinfo.guid_datastore_path
        return


    def _init(self):
        #
        super(Application, self)._init()
        # data root
        self.dds.dataroot = deploymentinfo.dataroot
        return



# example test case code. not a real one
import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        app = Application('main')
        app.run(self)
        return
#
def main():
    unittest.main()
    return
#
if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
