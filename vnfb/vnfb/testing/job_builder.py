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


    def main(self, computation, testFacility):
        self.testFacility = testFacility
        self.computation = computation
        
        db = self.db = self.clerk.db
        self.job = self.computation.getJob(db)

        self.buildjob()
        self.submitjob()
        return


    def buildjob(self):
        'test job building'
        # path
        dds = self.dds
        job = self.job
        db = self.db

        # reset job
        self._resetJob()
        
        # build job
        from vnfb.utils.job import buildjob
        computation = self.computation
        path = dds.abspath(job)
        buildjob(computation, db=db, dds=dds, path=path, director=self)

        # confirm
        self._checkJobDir()
        return


    def _checkJobDir(self):
        raise NotImplementedError


    def submitjob(self):
        "test job submission"

        testFacility = self.testFacility
        db = self.db
        dds = self.dds
        job = self.job

        # reset job
        self._resetJob()

        # reset itask
        itask = self._resetITask()

        # get the iworker that does the job submission
        iworker = self._retrieveIWorker()
        iworker.run(itask)
        
        return


    def declareProgress(self, fractional=None, message=None, percentage=None):
        if fractional is not None and percentage is not None:
            raise RuntimeError, "both fractional and percentage are supplied"
        if fractional is not None: percentage = fractional * 100
        print message, percentage
        return


    # helpers
    def _retrieveIWorker(self):
        iworker = self.retrieveComponent(
            'submitjob',
            factory='iworker',
            vault = ['iworkers'],
            )
        iworker.director = self
        return iworker

    
    def _resetJob(self):
        job = self.job
        dds = self.dds
        db  = self.db

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

        return
        

    def _resetITask(self):
        job = self.job
        db = self.db
        testFacility = self.testFacility
        
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
        return itask
    
            
    # following methods ensure to mimic the running environment of vnf application
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


# version
__id__ = "$Id$"

# End of file 
