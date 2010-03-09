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
Test of component job_builders/neutronexperiment.odb

Test assumes that
 1. database. see parameter "dbname"
 2. there is a neutronexperiment db record (with all the necessary associated records)
 3. there is a job db record for the neutronexperiment record

'''


#
from vnfb.testing import getDeploymentInfo
deploymentinfo = getDeploymentInfo()
dbname = deploymentinfo.dbname


#
dataroot = deploymentinfo.dataroot



# application
from luban.applications.UIApp import UIApp as base
class TestApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, expid, testFacility, *args, **kwds):
        self.domaccess = self.retrieveDOMAccessor('experiment')
        testFacility.assert_(self.domaccess is not None)
        self.testFacility = testFacility

        #
        self.computation = self.domaccess.getExperimentRecord(expid)
        db = self.db = self.domaccess.db
        self.job = self.computation.getJob(db)

        self.buildjob()
        self.submitjob()
        return


    def buildjob(self):
        # path
        dds = self.dds
        job = self.job
        db = self.db

        #
        path = dds.abspath(job)

        # remove the directory if it exists
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path)

        # remove the deps if it exist
        job.dependencies.clear(db)

        # build job
        from vnfb.utils.job import buildjob
        computation = self.computation
        buildjob(computation, db=db, dds=dds, path=path, director=self)

        # confirm
        # testFacility.assert_(os.path.exists(os.path.join(path, 'system')))
        # testFacility.assert_(os.path.exists(os.path.join(path, 'run.sh')))
        return


    def submitjob(self):
        "test job submission"

        testFacility = self.testFacility
        db = self.db
        dds = self.dds
        job = self.job
        
        # remove the directory if it exists
        path = dds.abspath(job)
        if os.path.exists(path):
            import shutil
            shutil.rmtree(path)

        # remove the deps if it exist
        job.dependencies.clear(db)

        # mark job as just created
        job.state = 'created'
        db.updateRecord(job)

        # find the itask
        from vnfb.dom.ITask import ITask
        gp = job.globalpointer
        gp = gp and gp.id
        if gp:
            itasks = db.query(ITask).filter_by(beneficiary=gp).all()
            if itasks:
                testFacility.assertEqual(len(itasks), 1)
                itask = itasks[0]
                # mark task as failed
                itask.state = 'failed'
                db.updateRecord(itask)
        else:
            # or create the itask
            itask = ITask()
            itask.id = 'itask-for-job-%s' % job.id
            itask.beneficiary = job
            db.insertRow(itask)

        # get the iworker that does the job submission
        iworker = self.retrieveComponent(
            'submitjob',
            factory='iworker',
            vault = ['iworkers'],
            )
        iworker.director = self
        iworker.run(itask)
        
        return


    def declareProgress(self, fractional=None, message=None, percentage=None):
        if fractional is not None and percentage is not None:
            raise RuntimeError, "both fractional and percentage are supplied"
        if fractional is not None: percentage = fractional * 100
        print message, percentage
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
        app.run('test-arcs-detector-system', self)
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
