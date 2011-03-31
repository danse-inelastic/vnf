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
    scheduler = schedulerfactory( server )
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath, suppressException=True)
    scheduler = scheduler(launch, prefix = 'source ~/.vnf > /dev/null' )

    # submit job through scheduler
    walltime = job.walltime
    from pyre.units.time import hour
    walltime = walltime*hour
    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath, walltime=walltime )

    # write id to the remote directory
    director.csaccessor.execute('echo "%s" > jobid' % id1, server, server_jobpath)

    # update job db record
    maxidlen = job.__class__.id_incomputingserver.length
    if len(id1) > maxidlen:
        msg = "The job id returned from scheduler exceeds the maximum length %s: id='%s'" %(
            maxidlen, id1)
        raise RuntimeError, msg
    job.id_incomputingserver = id1
    job.state = 'submitted'
    import time
    job.time_start = time.ctime()
    director.clerk.updateRecordWithID(job)
    
    return


def cancel( job, director ):
    "cancel a job"

    if job.state not in ['running']:
        return job

    oldstate = job.state
    
    #scheduler
    server = director.clerk.dereference(job.server)
    scheduler = schedulerfactory( server )

    #remote job path
    server_jobpath = director.dds.abspath(job, server=server)

    #
    launch = lambda cmd: director.csaccessor.execute(
        cmd, server, server_jobpath, suppressException=True)

    scheduler = scheduler(launch, prefix = 'source ~/.vnf' )

    scheduler.delete( job.id_incomputingserver )

    job.state = 'cancelled'
    director.clerk.updateRecordWithID( job )

    newstate = job.state

    if oldstate != newstate:
        # alert user
        user = director.clerk.getUser(job.creator)
        
        from vnf.utils.communications import announce
        announce(director, 'job-state-changed', job, user)
        
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


from vnf.components.CSAccessor import RemoteAccessError


# version
__id__ = "$Id$"

# End of file 
