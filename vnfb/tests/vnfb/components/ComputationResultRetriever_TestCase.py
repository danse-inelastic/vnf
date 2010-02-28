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


# job id.
jobid = "5WW9U3SR" 
# the computation is of type bvk_getdos


# result holder
from vnfb.dom.material_simulations.PhononDOS import PhononDOSTable as ResultHolder
result_holder_id = 'test-computationresultretriever'


# dummy retriever
from vnfb.components.ComputationResultRetriever import ComputationResultRetriever as base
class Retriever(base):

    pass



# application
from luban.applications.UIApp import UIApp as base
class TestApp(base):


    class Inventory(base.Inventory):

        import pyre.inventory


    def main(self, *args, **kwds):
        retriever = Retriever('test-retriever')
        retriever._initFacilitiesFromDirector(self)

        # get job and computation
        domaccessor = self.retrieveDOMAccessor('job')
        db = domaccessor.db
        from vnfb.dom.Job import Job
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

        retriever._save_results(
            computation, job, ['DOS'],
            result_holder,
            result_subdir = 'subdir',
            )
        
        return


    def _getPrivateDepositoryLocations(self):
        return ['../../../config', '../../../content/components', '/tmp/luban-services']


    def _configure(self):
        # db
        self.inventory.clerk.inventory.db = 'postgres:///vnfbeta'
        self.inventory.clerk._configure()
        #
        super(TestApp, self)._configure()
        return


    def _init(self):
        #
        super(TestApp, self)._init()
        # data root
        self.dds.dataroot = 'content/data'
        return
    

import unittest
class TestCase(unittest.TestCase):

    def test1(self):
        import dsaw.db
        app = TestApp('main')
        app.run()
        return

    

def main():
    unittest.main()
    return



if __name__ == '__main__': main()


# version
__id__ = "$Id$"

# End of file 
