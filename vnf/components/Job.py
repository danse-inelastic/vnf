#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Scheduler import schedule, check



def submit(job, director, debug=False):
    from vnf.utils import launch_detached, bindir
    import os
    exe = os.path.join(bindir, 'submitjob.py')
    launch_detached('%s -id=%s' % (exe, job.id), debug=debug)
    return


def pack(job, director, debug=False):
    from vnf.utils import launch_detached, bindir
    import os
    exe = os.path.join(bindir, 'packjobdir.py')
    launch_detached('%s -id=%s' % (exe, job.id), debug=debug)
    return


def data_manager( job, director ):
    from JobDataManager import JobDataManager
    return JobDataManager(job, director)


def new_job( director ):
    id = new_jobid( director )
    from vnf.dom.Job import Job
    job = Job()
    job.id = id
    director.clerk.newRecord( job )

    job.creator = director.sentry.username
    job.state = 'created'
    job.exit_code = -1
    import time
    job.time_start = job.time_completion = time.ctime()

    servers = director.clerk.getServers()
    server = servers[0]
    job.server = server

    job.numprocessors = 1
    director.clerk.updateRecord(job)
    
    return job


def isdone(job):
    return job.state in ['finished', 'cancelled', 'terminated']


from misc import new_id as new_jobid



# version
__id__ = "$Id$"

# End of file 
