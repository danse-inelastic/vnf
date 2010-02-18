# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2007-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



import journal
info = journal.info( 'scheduler' )


def schedule( job, director ):
    # copy local job directory to server
    server = director.clerk.dereference(job.server)
    server_jobpath = director.dds.abspath(job, server=server)

    # the server
    server = job.server.dereference(director.clerk.db)

    # the scheduler 
    Scheduler = schedulerfactory( server )
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath, suppressException=True)
    scheduler = Scheduler(launch, prefix = 'source ~/.vnf')

    # submit job through scheduler
    walltime = job.walltime
    from pyre.units.time import hour
    walltime = walltime*hour
    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath, walltime=walltime,
        jobid=job.id, numnodes = job.numnodes, corespernode = job.numcores,
        workingDirectory = server_jobpath)

    # write id to the remote directory
    director.csaccessor.execute('echo "%s" > jobid' % id1, server, server_jobpath)

    # update job db record
    job.id_incomputingserver = id1
    job.state = 'submitted'
    import time
    job.time_start = time.ctime()
    director.clerk.updateRecordWithID(job)
    
    return


def check( job, director ):
    "check status of a job"

    if job.state in ['finished', 'failed', 'terminated', 'cancelled']:
        return job

    oldstate = job.state
    
    #scheduler
    server = director.clerk.dereference(job.server)
    Scheduler = schedulerfactory( server )

    #remote job path
    server_jobpath = director.dds.abspath(job, server=server)

    #
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath, suppressException=True)

    scheduler = Scheduler(launch, prefix = 'source ~/.vnf')

    jobstatus = scheduler.status( job.id_incomputingserver )

    for k,v in jobstatus.iteritems():
        setattr(job, k, v)
        continue

    director.clerk.updateRecordWithID( job )

    newstate = job.state

    if oldstate != newstate:
        # alert user
        user = director.clerk.getUser(job.creator)
        
        from vnf.components.misc import announce
        announce(director, 'job-state-changed', job, user)
        
    return job


def cancel( job, director ):
    "cancel a job"

    if job.state not in ['running']:
        return job

    oldstate = job.state
    
    #scheduler
    server = director.clerk.dereference(job.server)
    Scheduler = schedulerfactory( server )

    #remote job path
    server_jobpath = director.dds.abspath(job, server=server)

    #
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath, suppressException=True)

    scheduler = Scheduler(launch, prefix = 'source ~/.vnf' )

    scheduler.delete( job.id_incomputingserver )

    job.state = 'cancelled'
    director.clerk.updateRecordWithID( job )

    newstate = job.state

    if oldstate != newstate:
        # alert user
        user = director.clerk.getUser(job.creator)
        
        from vnf.components.misc import announce
        announce(director, 'job-state-changed', job, user)
        
    return job



def schedulerfactory( server ):
    'obtain scheduler factory'
    #right now, scheduler info is saved in db record of the server
    schedulerType = server.scheduler
    if schedulerType in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from vnfb.clusterscheduler import scheduler as factory
    try: schedulerClass = factory(schedulerType)
    except: raise NotImplementedError, 'scheduler %r' % schedulerClass
    return schedulerClass


from CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
