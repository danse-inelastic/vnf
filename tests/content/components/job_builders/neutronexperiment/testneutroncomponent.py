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

    from vnfb.testing.job_builder import TestApp as base
    
    
    class TestApp(base):


        def main(self, testFacility):
            computation = self.createExp()
            return base.main(self, computation, testFacility)


        def createExp(self):
            director = self
            domaccess = self.retrieveDOMAccessor('experiment')
            orm = domaccess.orm
            db = orm.db
            
            # the instrument with source and monitor
            from vnfb.dom.neutron_experiment_simulations.Instrument import InstrumentTable
            instrument_record = db.query(InstrumentTable).filter_by(name='Test').one()
            instrument = orm.record2object(instrument_record)

            # create a new instrument configuration
            from vnfb.dom.neutron_experiment_simulations.InstrumentConfiguration import InstrumentConfiguration
            ic = InstrumentConfiguration()
            components = ic.components
            # source
            from vnfb.dom.neutron_experiment_simulations.neutron_components.MonochromaticSource import MonochromaticSource
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
            from vnfb.dom.neutron_experiment_simulations.NeutronExperiment import NeutronExperiment
            exp = NeutronExperiment()
            exp.instrument = instrument
            exp.instrument_configuration = ic
            exp.ncount = 10
            exp.buffer_size = 10
            exp.short_description = 'experiment for testing job builder of component %s' % Component.__name__
            orm.save(exp, save_not_owned_referred_object=0)
            exprecord = orm(exp)
            
            #
            # server
            serveraccess = director.retrieveDOMAccessor('server')
            server = serveraccess.getServerRecord('server000')

            # job
            from vnfb.dom.Job import Job
            job = Job()
            job.id = self.getGUID()
            job.short_description = 'job for test experiment for job builder of component %s' % Component.__name__
            job.server = server
            job.computation = exprecord
            job.creator = 'demo'
            orm.db.insertRow(job)

            return exprecord
        

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
    filename = '%s_TestCase.py' % comp.__name__
    open(filename, 'w').write(code)
    return filename



def skipComponents():
    from vnfb.dom.neutron_experiment_simulations.neutron_components.DetectorSystem_fromXML import DetectorSystem_fromXML
    from vnfb.dom.neutron_experiment_simulations.neutron_components.SNSModerator import SNSModerator
    from vnfb.dom.neutron_experiment_simulations.neutron_components.NeutronPlayer import NeutronPlayer
    from vnfb.dom.neutron_experiment_simulations.neutron_components.PlaceHolder import PlaceHolder
    from vnfb.dom.neutron_experiment_simulations.neutron_components.VanadiumPlate import VanadiumPlate
    from vnfb.dom.neutron_experiment_simulations.neutron_components.QMonitor import QMonitor
    return [
        DetectorSystem_fromXML,
        SNSModerator,
        NeutronPlayer,
        PlaceHolder,
        QMonitor
        ]


def createTestCasePyFiles():
    from vnfb.dom.neutron_experiment_simulations.neutron_components import findComponents
    comps = findComponents()
    return map(createTestCasePy, [c for c in comps if c not in skipComponents()])


from pyre.applications.Script import Script
class App(Script):

    class Inventory(Script.Inventory):
        
        import pyre.inventory
        component = pyre.inventory.str('component')
        all = pyre.inventory.bool('all')

    
    def main(self):
        if self.inventory.all:
            files = createTestCasePyFiles()
        else:
            component = self.inventory.component
            if not component:
                raise RuntimeError, 'component type is not specified'
            m = 'vnfb.dom.neutron_experiment_simulations.neutron_components.%s' % component
            m = __import__(m, {}, {}, [''])
            C = getattr(m, component)
            file = createTestCasePy(C)
            files = [file]

        import os
        for f in files:
            cmd = 'python %s' % f
            if os.system(cmd):
                raise RuntimeError, "%s failed" % f
            continue
        return

def main():
    app = App('test')
    app.run()
    return

if __name__ == '__main__': main()

# version
__id__ = "$Id$"

# End of file 
