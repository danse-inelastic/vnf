# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Instrument import Instrument
from SampleAssembly import SampleAssembly
from SampleEnvironment import SampleEnvironment
from Job import Job
from registry import tableRegistry


from OwnedObject import OwnedObject as base
class NeutronExperiment(base):

    name = 'neutronexperiments'

    import pyre.db

    instrument = pyre.db.reference( name = 'instrument', table = Instrument )
    instrument_configuration = pyre.db.versatileReference(
        name = 'instrument_configuration', tableRegistry = tableRegistry)

    # the following two references are used to define the sample
    # only one of them should be assigned.
    # sampleassembly is a more structured and extensible way to describe
    # the whole sample assembly at the sample position of a neutron instrument.
    # samplecomponent is a more straight-forward and quick way
    # to define a sample.
    sampleassembly = pyre.db.reference( name = 'sampleassembly', table = SampleAssembly )
    samplecomponent = pyre.db.versatileReference(name='samplecomponent', tableRegistry = tableRegistry)
    

    sampleenvironment = pyre.db.reference( name = 'sampleenvironment', table = SampleEnvironment )

    ncount = pyre.db.real( name = 'ncount', default = 1e6)

    constructed = pyre.db.varchar( name = 'constructed', length = 4, default = '' )

    job = pyre.db.reference( name = 'job', table = Job )

    status = pyre.db.varchar( name = 'status', length = 32, default = '' )
    # started: just started to be configured
    # partially configured: configuration not done
    # ready for submission: configuration done and ready for submission, job not created yet
    # constructed: configuration done and job created.
    # deleted: experiment is deleted

    expected_results = pyre.db.varcharArray( name = 'expected_results', length = 128 )
    

# version
__id__ = "$Id$"

# End of file 
