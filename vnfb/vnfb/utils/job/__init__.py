#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                     (C) 2007-2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from scheduler import schedule, check



def cancel(job, director):
    from scheduler import cancel
    return cancel(job, director)
    

def pack(job, director, debug=False):
    from vnfb.utils import launch_detached, bindir
    import os
    exe = os.path.join(bindir, 'packjobdir.py')
    launch_detached('%s -id=%s' % (exe, job.id), debug=debug)
    return


def new(director):
    from vnfb.dom.Job import Job
    job = director.clerk.insertNewOwnedRecord(Job)

    job.creator = director.sentry.username
    job.state = 'created'
    job.exit_code = -1
    import time
    job.time_start = job.time_completion = time.ctime()

    domaccess = director.retrieveDOMAccessor('server')
    servers = domaccess.getServerRecords()
    # assumption: there is at least 1 server
    server = servers[0]
    job.server = server
    
    job.numprocessors = 1
    director.clerk.updateRecordWithID(job)
    
    return job


def buildjob(computation, db=None, dds=None, path=None, director=None):
    name = computation.getJobBuilderName()
    builder = director.retrieveComponent(
        name,
        factory="job_builder", args=[name, path],
        vault=['job_builders'])
    builder.director = director
    files = builder.build(computation, db=db, dds=dds)
    deps = builder.getDependencies()
    return files, deps


def isdone(job):
    return job.state in ['finished', 'cancelled', 'terminated']


def isnew(job):
    return job.state in ['', 'created']


# version
__id__ = "$Id$"

# End of file 
