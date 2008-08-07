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


from OwnedObject import OwnedObject as base
class NeutronExperiment(base):

    name = 'neutronexperiments'

    import pyre.db

    instrument = pyre.db.reference( name = 'instrument', table = Instrument )

    sampleassembly = pyre.db.reference( name = 'sampleassembly', table = SampleAssembly )

    sampleenvironment = pyre.db.varchar( name = 'sampleenvironment', table = SampleEnvironment )

    ncount = pyre.db.real( name = 'ncount', default = 1e6)

    constructed = pyre.db.varchar( name = 'constructed', length = 4, default = '' )

    job = pyre.db.reference( name = 'job', table = Job )

    status = pyre.db.varchar( name = 'status', length = 16, default = '' )

    expected_results = pyre.db.varcharArray( name = 'expected_results', length = 128 )
    

# version
__id__ = "$Id$"

# End of file 
