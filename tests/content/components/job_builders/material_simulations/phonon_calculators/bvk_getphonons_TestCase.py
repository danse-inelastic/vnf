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
Test of component job_builders/material_simulations/phonon_calculators/bvk_getphonons

Test assumes that
 1. database. see parameter "dbname"
 2. there is a bvk_getphonons record and a job record for that computation

'''


#
from vnfb.testing import getDeploymentInfo
deploymentinfo = getDeploymentInfo()
dbname = deploymentinfo.dbname


#
dataroot = deploymentinfo.dataroot


# id for computation record.
recordid = "fortest" 


# application
from luban.applications.UIApp import UIApp as base
class TestApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, testFacility, *args, **kwds):
        self.domaccess = self.retrieveDOMAccessor('material_simulations/phonon_calculators/bvk')
        testFacility.assert_(self.domaccess is not None)
        self.testFacility = testFacility

        #
        computation = self.domaccess.getComputationRecord('phonons', recordid)
        db = self.domaccess.db
        job = computation.getJob(db)

        # path
        dds = self.dds
        path = dds.abspath(job)

        # remove the directory if it exists
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path)

        # build job
        from vnfb.utils.job import buildjob
        buildjob(computation, db=db, dds=dds, path=path, director=self)

        # confirm
        testFacility.assert_(os.path.exists(os.path.join(path, 'system')))
        testFacility.assert_(os.path.exists(os.path.join(path, 'run.sh')))
        return


    def _getPrivateDepositoryLocations(self):
        return deploymentinfo.pyre_depositories


    def _configure(self):
        # db
        self.inventory.clerk.inventory.db = dbname
        self.inventory.clerk._configure()
        #
        super(TestApp, self)._configure()
        return


    def _init(self):
        #
        super(TestApp, self)._init()
        # data root
        self.dds.dataroot = dataroot
        return


import os


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
