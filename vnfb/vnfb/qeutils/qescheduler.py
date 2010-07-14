#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from vnfb.qeutils.qeconst import NOPARALLEL
import math

PROC_PER_NODE   = 12    # Number of processors per node, specific for foxtrot

# Temp solution for QE jobs submission. Hardcoded for the foxtrot cluster
# param: job (input -> temp solution)

# XXX: Make the wall time configurable
def schedule( sim, director, job ):
    # TODO: Change status of jobs depending on the scheduling steps
    # copy local job directory to server
    server          = director.clerk.getServers(id=job.serverid)    # not None
    settingslist    = director.clerk.getQESettings(where="simulationid='%s'" % sim.id)
    task            = director.clerk.getQETasks(id=job.taskid)  # not None
    settings        = settingslist[0]   # not None
    server_jobpath  = director.dds.abspath(job, server=server)

    # the scheduler
    scheduler = schedulerfactory( server )
    launch = lambda cmd: director.csaccessor.execute(
                                                    cmd,
                                                    server,
                                                    server_jobpath,
                                                    suppressException=True)
    scheduler = scheduler(launch, prefix = 'source ~/.vnf' )
#    scheduler.setSimulationParams(job, settings, server, task)
#    dir     = ""    # Working directory

    from pyre.units.time import hour
    walltime = 999*hour   # limit to one hour?
    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath,
                            walltime        = walltime,
                            jobid           = jobid(job),
                            numnodes        = nodes(settings, task),
                            corespernode    = ppn(settings, task),
                            workingDirectory = workDir(server, job))

    # write id to the remote directory
    director.csaccessor.execute('echo "%s" > jobid' % id1, server, server_jobpath)

    return


## Specific for Quantum Espresso
#def setSimulationParams(self, job, settings, server, task):
#    "Set simulation objects"
#    self._job       = job       # not None
#    self._settings  = settings  # not None
#    self._server    = server    # not None
#    self._task      = task      # not None

def jobid(job):
    "Returns job id"
    if not job:
        return ""

    return job.id


def nodes(settings, task):
    "Returns number of nodes"
    n  = getnodes(settings)

    if task and task.type in NOPARALLEL:
        n  = 1

    return n


def getnodes(settings):
    "Calculates number of nodes (nodes) from number of processors"
    if not settings:
        return 1
    
    numproc = settings.numproc
    return int(math.ceil(numproc/float(PROC_PER_NODE)))


def ppn(settings, task):
    "Returns number of processors per node"
    ppn = getppn(settings)
    if task and task.type in NOPARALLEL:
        ppn  = 1

    return ppn


def getppn(settings):
    "Calculates number of processors per node (ppn) from number of processors"
    if not settings:
        return 1
    
    numproc = settings.numproc
    if numproc <= PROC_PER_NODE:
        return numproc

    return PROC_PER_NODE


def workDir(server, job):
    "Returns working directory (where the outputs are stored)"
    if not server or not job:
        return "/tmp"   # Default directory

    return "%s/%s/%s" % (server.workdir, job.name, job.id)


def schedulerfactory( server ):
    'obtain scheduler factory'
    #right now, scheduler info is saved in db record of the server
    scheduler = server.scheduler
    if scheduler in [ None, '', 'None' ]:
        raise RuntimeError, "scheduler not specified"

    from vnfb.clusterscheduler import scheduler as factory
    try: scheduler = factory( scheduler )
    except: raise NotImplementedError, 'scheduler %r' % scheduler
    return scheduler


__date__ = "$Dec 7, 2009 8:45:49 AM$"


# ********************* DEAD CODE ********************* 

    # submit job through scheduler
    #walltime = job.walltime

    # update job db record
#    job.id_incomputingserver = id1
#    job.state = 'submitted'
#    import time
#    job.time_start = time.ctime()
#    director.clerk.updateRecordWithID(job)
