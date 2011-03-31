# -*- Python -*-
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


from Instrument import Instrument
from InstrumentConfiguration import InstrumentConfiguration
from SampleAssembly import SampleAssembly
from SampleEnvironment import SampleEnvironment


class NeutronExperiment:

    # instrument
    instrument = None
    instrument_configuration = None

    # sample
    sample = None
    sample_configuration = None

    # sample environment
    sampleenvironment = None
    
    ncount = 1e6
    buffer_size = 1e5
    short_description = 'experiment description'

    def customizeLubanObjectDrawer(self, drawer):
        drawer.sequence = [
            'instrument_configuration',
            'sample_configuration',
            'sampleenvironment',
            'properties',
            ]
        drawer.mold.sequence = ['short_description', 'ncount', 'buffer_size']


from instrument_configuration_types import getTypes
instrument_configuration_types = getTypes()
instrument_configuration_types.append(InstrumentConfiguration)


from samplecomponent_types import getTypes
samplecomponent_types = getTypes()
sample_types = [SampleAssembly] + samplecomponent_types


from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    dbtablename = 'neutronexperiments'

    instrument = InvBase.d.reference(
        name = 'instrument', targettype = Instrument, owned = 0)
    instrument_configuration = InvBase.d.reference(
        name = 'instrument_configuration',
        targettypes = instrument_configuration_types,
        owned = 1,
        )

    sample = InvBase.d.reference(
        name = 'sample',
        targettype=None,
        targettypes = sample_types,
        owned = 0)
    # sample_configuration is the configuration of the sample
    # separation of sample and sample_configuration simplifies implementation of
    # manipulations of sample configuration.
    # sample_configuration is implemented using the same data object types as
    # sample. in db, sample_configuration just has its column "isconfiguration"
    # marked as true.
    # please also read neutron_components.SampleBase
    sample_configuration = InvBase.d.reference(
        name = 'sample_configuration',
        targettypes = sample_types,
        owned = 1,
        )
    
    sampleenvironment = InvBase.d.reference(
        name = 'sampleenvironment', targettype = SampleEnvironment, owned = 1)

    ncount = InvBase.d.float(name = 'ncount', default = 1e6)
    buffer_size = InvBase.d.int(name = 'buffer_size', default = 100000)
    short_description = InvBase.d.str(
        name='short_description', default='experiment description',
        max_length = 128,
        validator=InvBase.v.notempty)

    # constructed = InvBase.d.varchar( name = 'constructed', length = 4, default = '' )

    # status = InvBase.d.varchar( name = 'status', length = 32, default = '' )
    # started: just started to be configured
    # partially configured: configuration not done
    # ready for submission: configuration done and ready for submission, job not created yet
    # constructed: configuration done and job created.
    # deleted: experiment is deleted

    # expected_results = InvBase.d.varcharArray( name = 'expected_results', length = 128 )

NeutronExperiment.Inventory = Inventory
del Inventory


from _ import o2t, ComputationTableBase as TableBase
NeutronExperimentTable = o2t(NeutronExperiment, {'subclassFrom': TableBase})
NeutronExperimentTable.job_builder = 'neutronexperiment'
NeutronExperimentTable.actor = 'experiment'

# version
__id__ = "$Id$"

# End of file 
