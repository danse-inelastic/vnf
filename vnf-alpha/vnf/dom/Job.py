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

from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base
class Job(base):

    name = 'jobs'

    import dsaw.db
    
    server = dsaw.db.reference( name='server', table = Server)

    time_completion = dsaw.db.timestamp(name='time_completion')
    time_completion.meta['tip'] = 'time left to completion'
    
    time_start = dsaw.db.timestamp(name='time_start')
    time_start.meta['tip'] = 'the time the job started'
    
    numprocessors = dsaw.db.integer(name='numprocessors', default = 1)
    numprocessors.meta['tip'] = 'the number of processors this job uses'

    walltime = dsaw.db.integer(name='walltime', default = 1)
    walltime.meta['tip'] = 'limit of wall time. unit: hour'

    id_incomputingserver = dsaw.db.varchar(name="id_incomputingserver", length=64)
    id_incomputingserver.meta['tip'] = "the id of this job when submitted to the computing server. this is given by the computing server."

    state = dsaw.db.varchar( name = 'state', length = 16 )
    # state:
    #   - created: just created. has not been submitted
    #   - submitted
    #   - submitting
    #   - submissionfailed
    #   - running
    #   - onhold
    #   - finished
    #   - terminated
    #   - cancelled

    remote_outputfilename = dsaw.db.varchar(
        name = 'remote_outputfilename', length = 512 )
    remote_errorfilename = dsaw.db.varchar(
        name = 'remote_errorfilename', length = 512 )

    output = dsaw.db.varchar(name = 'output', length = 2048)
    error = dsaw.db.varchar(name = 'error', length = 2048)
    
    exit_code = dsaw.db.integer(name = 'exit_code', default = -1)

    computation = dsaw.db.versatileReference(
        name = 'computation')
    computation.meta['tip'] = 'The type of computation'

    import vnf.dom
    dependencies = vnf.dom.referenceSet(name='dependencies')

    # pending internal-tasks to get this job going
    pending_tasks = vnf.dom.referenceSet(name='pending_tasks')


# version
__id__ = "$Id$"

# End of file 
