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
factory to create test case for job builder of one neutron component

Test assumes that
 1. database. see parameter "dbname"

'''


def createTestApp(Component):

    from vnf.testing.job_builder import TestApp as base
    
    
    class TestApp(base):


        def main(self, testFacility):
            # get the test experiment
            computation = self.getExp()
            #
            return base.main(self, computation, testFacility)


        def getExp(self):
            director = self
            domaccess = self.retrieveDOMAccessor('experiment')
            orm = domaccess.orm
            db = orm.db
            
            # see if the experiment is already in db
            expid = 'testjobbuilder-component-%s' % Component.__name__
            from vnf.dom.neutron_experiment_simulations.NeutronExperiment import NeutronExperimentTable
            exps = db.query(NeutronExperimentTable).filter_by(id=expid).all()

            if not exps:
                # no test experiment for this component yet, create a new experiment
                exp = self.createExp(expid, db)
            else:
                if len(exps)>1: raise RuntimeError, 'should not happen: more than one exps'
                exp = exps[0]
            return exp


        def createExp(self, expid, db):
            director = self
            domaccess = self.retrieveDOMAccessor('experiment')
            orm = domaccess.orm
            db = orm.db
            
            # the instrument with source and monitor
            from vnf.dom.neutron_experiment_simulations.Instrument import InstrumentTable
            instrument_record = db.query(InstrumentTable).filter_by(name='Test').one()
            instrument = orm.record2object(instrument_record)

            # create a new instrument configuration
            from vnf.dom.neutron_experiment_simulations.InstrumentConfiguration import InstrumentConfiguration
            ic = InstrumentConfiguration()
            components = ic.components
            # source
            from vnf.dom.neutron_experiment_simulations.neutron_components.MonochromaticSource import MonochromaticSource
            source = MonochromaticSource()
            source.componentname = 'source'
            source.energy = 70
            ic.components.append(source)

            # component to test
            comp2 = Component()
            comp2.componentname = 'component2'
            ic.components.append(comp2)
            #
            
            # experiment
            from vnf.dom.neutron_experiment_simulations.NeutronExperiment import NeutronExperiment
            exp = NeutronExperiment()
            exp.instrument = instrument
            exp.instrument_configuration = ic
            exp.ncount = 10
            exp.buffer_size = 10
            exp.short_description = 'experiment for testing job builder of component %s' % Component.__name__
            orm.save(exp, save_not_owned_referred_object=0, id=expid)
            exprecord = orm(exp)
            
            # job
            jobid = 'testjobbuilder-neutroncomponent-%s' % Component.__name__
            from vnf.dom.Job import Job
            jobs = orm.db.query(Job).filter_by(id=jobid).all()
            if not jobs:
                job = self.createJob(jobid, exprecord, orm.db)
            else:
                if len(jobs)>1: raise RuntimeError, 'should not happen: more than one jobs'
                job = jobs[0]
                job.computation = exprecord
                orm.db.updateRecord(job)
                
            return exprecord

        
        def createJob(self, id, exprecord, db):
            # server
            serveraccess = self.retrieveDOMAccessor('server')
            server = serveraccess.getServerRecord('server000')
            
            from vnf.dom.Job import Job
            job = Job()
            job.id = id
            job.short_description = 'job for test experiment for job builder of component %s' % Component.__name__
            job.server = server
            job.computation = exprecord
            job.creator = 'demo'
            db.insertRow(job)
            return
            

        def _checkJobDir(self):
            return

    return TestApp


def createTestCase(Component):
    import unittest
    class TestCase(unittest.TestCase):

        def test1(self):
            name = 'test-jobbuilder-%s' % Component.__name__
            name = 'main'
            App = createTestApp(Component)
            app = App(name)
            app.run(self)
            return

    return TestCase


def createTestCasePy(comp):
    'comp: component class'
    code = '''
standalone = True
from testneutroncomponent import createTestCase
from %s import %s
TestCase = createTestCase(%s)
def main():
    import unittest
    unittest.main()
    return
if __name__ == '__main__': main()
    ''' % (comp.__module__, comp.__name__, comp.__name__)
    filename = getTestCasePyFilename(comp)
    open(filename, 'w').write(code)
    return filename


def getTestCasePyFilename(comp):
    return '%s_TestCase.py' % comp.__name__



def skipComponents():
    from vnf.dom.neutron_experiment_simulations.neutron_components.DetectorSystem_fromXML import DetectorSystem_fromXML
    from vnf.dom.neutron_experiment_simulations.neutron_components.SNSModerator import SNSModerator
    from vnf.dom.neutron_experiment_simulations.neutron_components.NeutronPlayer import NeutronPlayer
    from vnf.dom.neutron_experiment_simulations.neutron_components.PlaceHolder import PlaceHolder
    from vnf.dom.neutron_experiment_simulations.neutron_components.VanadiumPlate import VanadiumPlate
    from vnf.dom.neutron_experiment_simulations.neutron_components.QMonitor import QMonitor
    return [
        DetectorSystem_fromXML,
        SNSModerator,
        NeutronPlayer,
        PlaceHolder,
        VanadiumPlate,
        QMonitor
        ]


def createTestCasePyFiles():
    from vnf.dom.neutron_experiment_simulations.neutron_components import findComponents
    comps = findComponents()
    return map(createTestCasePy, [c for c in comps if c not in skipComponents()])

def getTestCasePyFiles():
    from vnf.dom.neutron_experiment_simulations.neutron_components import findComponents
    comps = findComponents()
    return map(getTestCasePyFilename, [c for c in comps if c not in skipComponents()])


def runTestCases(files):
    import os
    for f in files:
        print 'running test %s' % f
        cmd = 'python %s' % f
        if os.system(cmd):
            cleanTestCases()
            raise RuntimeError, "%s failed" % f
        continue
    cleanTestCases()
    return


def cleanTestCases():
    files = getTestCasePyFiles()
    import os
    for f in files:
        if os.path.exists(f):
            os.remove(f)
        continue
    return


from pyre.applications.Script import Script
class App(Script):

    class Inventory(Script.Inventory):
        
        import pyre.inventory
        component = pyre.inventory.str('component')
        all = pyre.inventory.bool('all')
        clean = pyre.inventory.bool('clean')

    
    def main(self):
        if self.inventory.clean:
            self.clean()
            return

        if self.inventory.all:
            files = createTestCasePyFiles()
        else:
            component = self.inventory.component
            if not component:
                raise RuntimeError, 'component type is not specified'
            m = 'vnf.dom.neutron_experiment_simulations.neutron_components.%s' % component
            m = __import__(m, {}, {}, [''])
            C = getattr(m, component)
            file = createTestCasePy(C)
            files = [file]
        
        runTestCases(files)
        return

    
    def clean(self):
        cleanTestCases()
        return


def main():
    app = App('test')
    app.run()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
