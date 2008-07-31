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
    manager = JobDataManager( job, director )

    # copy local job directory to server
    manager.initremotedir( )
    server_jobpath = manager.remotepath()

    # the server
    server = job.computation_server

    scheduler = schedulerfactory( server )
    scheduler = scheduler(
        lambda cmd: director.csaccessor.execute( cmd, server, server_jobpath ),
        prefix = 'source ~/.vnf' )
    
    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath )
    job.id_incomputingserver = id1

    import time
    job.timestart = time.ctime()

    director.clerk.updateRecord( job )
    
    return


def check( job, director ):
    "check status of a job"

    if job.status == 'finished': return job

    from JobDataManager import JobDataManager
    manager = JobDataManager( job, director )

    #scheduler
    scheduler = schedulerfactory( job.computation_server )

    #remote job path
    server_jobpath = manager.remotepath()

    #
    server = job.computation_server
    
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath )

    scheduler = scheduler(
        launch,
        prefix = 'source ~/.vnf' )

    jobstatus = scheduler.status( job )

    for k,v in jobstatus.iteritems():
        setattr(job, k, v)
        continue

    director.clerk.updateRecord( job )
    return job


def schedulerfactory( server ):
    'obtain scheduler factory'
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
