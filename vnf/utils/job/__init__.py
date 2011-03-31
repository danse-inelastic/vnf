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


import journal
info = journal.info('job')


from scheduler import schedule


def check( job, director ):
    "check status of a job"

    info.log('checking status of job %s' % job.id)
    
    if job.state in ['finished', 'failed', 'terminated', 'cancelled']:
        return job

    oldstate = job.state
    
    # scheduler factory
    server = director.clerk.dereference(job.server)
    import scheduler
    schedulerfactory = scheduler.schedulerfactory( server )

    # remote job path
    server_jobpath = director.dds.abspath(job, server=server)

    # launcher
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath, suppressException=True)

    # scheduler
    scheduler = schedulerfactory(launch, prefix = 'source ~/.vnf' )

    # get status
    jobstatus = scheduler.status( job.id_incomputingserver )
    # 
    for k,v in jobstatus.iteritems():
        setattr(job, k, v)
        continue
    # update
    director.clerk.updateRecordWithID( job )

    # new status
    newstate = job.state

    #
    if oldstate != newstate:
        # state changed 
        info.log('job %s: state changed from %r to %r' % (
            job.id, oldstate, newstate))

        # alert user
        user = director.clerk.getUser(job.creator)
        from vnf.utils.communications import announce
        announce(director, 'job-state-changed', job, user)

        # callback
        try:
            callback = eval('on%s'%newstate)
        except:
            pass
        else:
            callback(job, director)
        
    return job


# event handlers
def onfinished(job, director):
    info.log('onfinished: %s' % job.id)
    # when a job finished, should try to retrieve results from
    
    # 1. get the computation
    db = director.clerk.db
    computation = job.computation.dereference(db)

    # 2. retrieve
    from vnf.utils.computation import start_results_retrieval
    start_results_retrieval(computation, director)
    return


def onterminated(job, director):
    info.log('onterminated: %s' % job.id)
    # terminated means we don't really know if the job finished without error
    # right now let us just pretend it does and let the result retriever handle
    # errors if there are any
    return onfinished(job, director)



#
def cancel(job, director):
    from scheduler import cancel
    return cancel(job, director)
    

def pack(job, director, debug=False):
    from vnf.utils import launch_detached, bindir
    import os
    exe = os.path.join(bindir, 'packjobdir.py')
    launch_detached('%s -id=%s' % (exe, job.id), debug=debug)
    return


def new(director):
    from vnf.dom.Job import Job
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
