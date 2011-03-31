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

from vnf.qeutils.qeconst import NOPARALLEL
from pyre.units.time import hour
import math
import os

PROC_PER_NODE   = 12        # Number of processors per node, specific for foxtrot
TEMP_DIR        = "/tmp"    # Temp default directory
VAR_SET_FILE    = "~/.vnf"  # File for setting environmental variables and adding modules
JOB_ID          = "jobid"   # File where the job id is stored

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
    scheduler = scheduler(launch, prefix = "source %s" % VAR_SET_FILE )
    walltime = 999*hour   # limit to one hour?

    id1 = scheduler.submit( 'cd %s && sh run.sh' % server_jobpath,
                            walltime        = walltime,
                            jobid           = jobid(job),
                            numnodes        = nodes(settings, task),
                            corespernode    = ppn(settings, task),
                            workingDirectory = workDir(server, job))

    # write id to the remote directory
    director.csaccessor.execute('echo "%s" > %s' % (id1, JOB_ID) , server, server_jobpath)

    return


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
    "Returns working directory (where the outputs are stored) which is qejobs"
    if not server or not job:
        return TEMP_DIR   # Default directory

    return os.path.join(server.workdir, job.name, job.id) # "%s/%s/%s" % (server.workdir, job.name, job.id)


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


__date__ = "$Dec 7, 2009 8:45:49 AM$"
