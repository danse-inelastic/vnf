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



import journal
info = journal.info( 'scheduler' )


def schedule( job, director ):
    from JobDataManager import JobDataManager
    manager = JobDataManager( job, director.db, director.csaccessor )

    # copy local job directory to server
    manager.initremotedir( )
    server_jobpath = manager.remotepath()

    # the server
    server = job.server.dereference(director.db)

    # the scheduler 
    scheduler = schedulerfactory( server )
    scheduler = scheduler(
        lambda cmd: director.csaccessor.execute( cmd, server, server_jobpath ),
        prefix = 'source ~/.vnf' )

    # submit job through scheduler
    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath )

    # write id to the remote directory
    director.csaccessor.execute( 'echo "%s" > jobid' % id1, server, server_jobpath )

    # update job db record
    job.id_incomputingserver = id1
    job.state = 'submitted'
    import time
    job.time_start = time.ctime()
    director.clerk.updateRecord( job )
    
    return


def check( job, director ):
    "check status of a job"

    if job.state in ['finished', 'failed', 'terminated']:
        return job

    #scheduler
    server = job.server.dereference(director.db)
    scheduler = schedulerfactory( server )

    #remote job path
    from JobDataManager import JobDataManager
    manager = JobDataManager(job, director.db)
    server_jobpath = manager.remotepath()

    #
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath )

    scheduler = scheduler(
        launch,
        prefix = 'source ~/.vnf' )

    jobstatus = scheduler.status( job.id_incomputingserver )

    for k,v in jobstatus.iteritems():
        setattr(job, k, v)
        continue

    director.clerk.updateRecord( job )
    return job


def schedulerfactory( server ):
    'obtain scheduler factory'
    #right now, scheduler info is saved in db record of the server
    scheduler = server.scheduler
    if scheduler in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from vnf.clusterscheduler import scheduler as factory
    try: scheduler = factory( scheduler )
    except: raise NotImplementedError, 'scheduler %r' % scheduler
    return scheduler


from CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
