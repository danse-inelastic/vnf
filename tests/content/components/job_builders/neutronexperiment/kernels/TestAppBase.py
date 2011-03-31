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


from vnfb.testing.job_builder import TestApp as base
class TestAppBase(base):

    Kernel = None


    class Inventory(base.Inventory):

        import pyre.inventory
        
        server = pyre.inventory.str('server')
        
    
    def getKernel(self):
        raise Notimplementedactor


    def main(self, testFacility):
        # get the test experiment
        computation = self.getExp()
        #
        return base.main(self, computation, testFacility)


    def getExp(self):
        Kernel = self.Kernel

        director = self
        domaccess = self.retrieveDOMAccessor('experiment')
        orm = domaccess.orm
        db = orm.db
        
        # see if the experiment is already in db
        expid = 'testjobbuilder-kernel-%s' % Kernel.__name__
        from vnfb.dom.neutron_experiment_simulations.NeutronExperiment import NeutronExperimentTable
        exps = db.query(NeutronExperimentTable).filter_by(id=expid).all()

        if not exps:
            # no test experiment for this component yet, create a new experiment
            exp = self.createExp(expid, db)
        else:
            if len(exps)>1: raise RuntimeError, 'should not happen: more than one exps'
            exp = exps[0]
        
        if self.inventory.server:
            self.updateJobServer(exp)

        return exp


    def createExp(self, expid, db):
        director = self
        domaccess = self.retrieveDOMAccessor('experiment')
        orm = domaccess.orm
        db = orm.db

        # the instrument with source and monitor
        from vnfb.dom.neutron_experiment_simulations.Instrument import InstrumentTable
        instrument_record = db.query(InstrumentTable).filter_by(name='IdealPowderINS').one()
        instrument = orm.record2object(instrument_record)

        # instrument configuration
        from vnfb.dom.neutron_experiment_simulations.InstrumentConfiguration import InstrumentConfiguration
        ic = InstrumentConfiguration()
        ic.components = instrument.components

        # create a new sample assembly
        from vnfb.dom.neutron_experiment_simulations.SampleAssembly import SampleAssembly
        sampleassembly = SampleAssembly()
        
        # create a scatterer
        from vnfb.dom.neutron_experiment_simulations.Scatterer import Scatterer
        scatterer = Scatterer(); scatterer.scatterername = 'sample'
        # add scatterer to sample assembly
        sampleassembly.scatterers = [scatterer]
        
        # more details about the scatterer
        # shape
        from vnfb.dom.geometry.Block import Block
        scatterer.shape = orm.load(Block, id='default-sample-plate-1')
        # matter
        from vnfb.dom.AtomicStructure import StructureTable
        where = "short_description like '%bcc Fe at 295%'"
        struct = orm.db.query(StructureTable).filter(where).all()[0]
        matter = orm.record2object(struct)
        scatterer.matter = matter
        # create a kernel
        kernel = self.getKernel(); kernel.matter = matter
        scatterer.kernels = [kernel]

        # experiment
        from vnfb.dom.neutron_experiment_simulations.NeutronExperiment import NeutronExperiment
        exp = NeutronExperiment()
        exp.instrument = instrument
        exp.instrument_configuration = ic
        exp.sample_configuration = sampleassembly
        exp.ncount = 10
        exp.buffer_size = 10
        exp.short_description = 'experiment for testing job builder of kernel %s' % self.Kernel.__name__
        orm.save(exp, save_not_owned_referred_object=0, id=expid)

        # job
        job = self.getJob(exp)
        return orm(exp)
        

    def getJob(self, exp):
        director = self
        domaccess = self.retrieveDOMAccessor('experiment')
        orm = domaccess.orm

        #
        exprecord = orm(exp)

        # job
        from vnfb.dom.Job import Job
        jobid = 'testjobbuilder-kernel-%s' % self.Kernel.__name__
        if len(jobid) > Job.id.length:
            jobid = ('%s-testjbkernel' % self.Kernel.__name__)[:Job.id.length]
        jobs = orm.db.query(Job).filter_by(id=jobid).all()
        if not jobs:
            job = self.createJob(jobid, exprecord, orm.db)
        else:
            if len(jobs)>1: raise RuntimeError, 'should not happen: more than one jobs'
            job = jobs[0]
            job.computation = exprecord
            orm.db.updateRecord(job)
        return job


    def updateJobServer(self, exprecord):
        director = self
        domaccess = self.retrieveDOMAccessor('experiment')
        orm = domaccess.orm
        
        # job record
        job = exprecord.getJob(orm.db)
        
        # update
        job.server = self._getServer()
        orm.db.updateRecord(job)
        
        return
        

    def createJob(self, id, exprecord, db):
        # server
        server = self._getServer()
        
        #
        from vnfb.dom.Job import Job
        job = Job()
        job.id = id
        job.short_description = 'job for test experiment for job builder of component %s' % self.Kernel.__name__
        job.server = server
        job.computation = exprecord
        job.creator = 'demo'
        db.insertRow(job)
        return job


    def _getServer(self):
        serveraccess = self.retrieveDOMAccessor('server')
        server = self.inventory.server or 'server000'
        return serveraccess.getServerRecord(server)


    def _checkJobDir(self):
        return



def createTestCase(App):
    import unittest
    class TestCase(unittest.TestCase):

        def test1(self):
            name = 'main'
            app = App(name)
            app.run(self)
            return

    return TestCase


# version
__id__ = "$Id$"

# End of file 
