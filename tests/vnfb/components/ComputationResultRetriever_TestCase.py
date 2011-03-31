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
Test of methods of base class vnf.components.ComputationResultRetriever.ComputationResultRetriever.

Test assumes that
 1. database. see parameter "dbname"
 2. there is a bvk_getdos record in the db that has finished. and in the data directory
    for the job associated with the bvk_getdos computation, there is a data file "DOS".
 3. There is a table "phonondoses"
 4. This directory is writable.

The test cases here will try to do things like retrieve results in the job directory
to local data directory
'''


skip = True # temporarily let auto testing to skip over this test.


#
from vnf.testing import getDeploymentInfo
deploymentinfo = getDeploymentInfo()
dbname = deploymentinfo.dbname


#
dataroot = deploymentinfo.dataroot


# job id.
jobid = "5WW9U3SR" 
# the computation is of type bvk_getdos


# result holder
from vnf.dom.material_simulations.PhononDOS import PhononDOSTable as ResultHolder
result_holder_id = 'test-computationresultretriever'


# dummy retriever
from vnf.components.ComputationResultRetriever import ComputationResultRetriever as base
class Retriever(base):

    pass



# application
from luban.applications.UIApp import UIApp as base
class TestApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, testFacility, *args, **kwds):
        retriever = Retriever('test-retriever')
        retriever._initFacilitiesFromDirector(self)

        # get job and computation
        domaccessor = self.retrieveDOMAccessor('job')
        db = domaccessor.db
        from vnf.dom.Job import Job
        job = domaccessor.getRecordByID(Job, jobid)
        computation = db.dereference(job.computation)

        # result holder
        try:
            result_holder = domaccessor.getRecordByID(ResultHolder, result_holder_id)
        except:
            result_holder = ResultHolder()
            result_holder.id = result_holder_id
            domaccessor.db.insertRow(result_holder)
            
        result_holder.id = 'test-computationresultretriever'

        subdir = 'subdir'
        retriever._save_results(
            computation, job, ['DOS'],
            result_holder,
            result_subdir = subdir,
            )

        testFacility.assert_(os.path.exists(self.dds.abspath(result_holder)))
        p = os.path.join(self.dds.abspath(result_holder), subdir)
        testFacility.assert_(os.path.exists(p))
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

        #
        if os.path.exists(dataroot):
            import shutil
            shutil.rmtree(dataroot)
        return


import os


import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        import dsaw.db
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
