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


from registry import tableRegistry
from Server import Server

from OwnedObject import OwnedObject as base
class Job(base):

    name = 'jobs'

    import pyre.db
    
    server = pyre.db.reference( name='server', table = Server)

    time_completion = pyre.db.timestamp(name='time_completion')
    time_completion.meta['tip'] = 'time left to completion'
    
    time_start = pyre.db.timestamp(name='time_start')
    time_start.meta['tip'] = 'the time the job started'
    
    numprocessors = pyre.db.integer(name='numprocessors', default = 1)
    numprocessors.meta['tip'] = 'the number of processors this job uses'

    id_incomputingserver = pyre.db.varchar(name="id_incomputingserver", length=100)
    id_incomputingserver.meta['tip'] = "the id of this job when submitted to the computing server. this is given by the computing server."

    state = pyre.db.varchar( name = 'state', length = 16 )
    # state:
    #   - created: just created. has not been submitted
    #   - submitted
    #   - running
    #   - onhold
    #   - finished
    #   - terminated
    #   - cancelled

    remote_outputfilename = pyre.db.varchar(
        name = 'remote_outputfilename', length = 512 )
    remote_errorfilename = pyre.db.varchar(
        name = 'remote_errorfilename', length = 512 )

    output = pyre.db.varchar(name = 'output', length = 2048)
    error = pyre.db.varchar(name = 'error', length = 2048)
    
    exit_code = pyre.db.integer(name = 'exit_code', default = -1)

    computation = pyre.db.versatileReference(
        name = 'computation', tableRegistry = tableRegistry)
    computation.meta['tip'] = 'The compuation that this job is about'


# version
__id__ = "$Id$"

# End of file 
