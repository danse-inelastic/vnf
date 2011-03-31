# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from luban.content import load, select
import luban.content as lc
from vnf.epscutils.epscconst import FILETYPE
from vnf.qeutils.qeutils import latestInput, latestJob

def settingsLink(director, id):
    "Returns link to settings of simulation"
    settings  = director.clerk.getQESettings(where="simulationid='%s'" % id )

    # Default link
    link = lc.link(label="Create",
                Class="epsc-action-create",
                tip     = "Set simulation environment",
                onclick=load(actor      = "material_simulations/epsc/settings-add",
                             id         = id))

    if settings:
        s = settings[0]
        if s:
            link = lc.link(label   = s.sname,
                        Class   = "action-link",
                        onclick = load(actor    = "material_simulations/epsc/settings-view",
                                     id         = id,
                                     configid   = s.id))

    return link



def serverLink(director, id):
    "Returns link to server information"
    server = None
    link = "None"

    settings    = director.clerk.getQESettings(where="simulationid='%s'" % id )
    if not settings:# or not settings[0]:
        return link

    setting     = settings[0]
    server = director.clerk.getServers(id = setting.serverid )

    if not server:
        return link


    link = lc.link(label   = server.address,
                Class   = "action-link",
                tip     = "Show details of computational cluster",
                onclick = select(id='').append(load(actor='server/load', routine='createDialog'))
                )

    return link


def configLink(director, id, taskid, type, structureid):
    "Returns link to configuration"
    if not type in FILETYPE:    # Extra protection :)
        return "None"

    inputs  = director.clerk.getQEConfigurations(where="taskid='%s' and type='%s'" % (taskid, type))
    actorName   = "material_simulations/epsc/%s-create" % type
    # Default link
    link = lc.link(label="Create",
                   Class="epsc-action-create",
                   onclick=load(actor      = actorName,
                             id         = id,
                             taskid     = taskid,
                             type       = type,
                             structureid = structureid))
                             
    if not inputs:      # No inputs created, return "Add" link
        return link

    input   = latestInput(inputs)
    if not input:       # No input, return default link
        return link

    # Link to configuration view
    return lc.link(label   = input.filename,
                   onclick = load(actor      = "material_simulations/epsc/config-view",
                               id         = id,
                               taskid     = taskid,
                               type       = type,
                               configid   = input.id))


def runLink(director, id, taskid):
    "Returns run link"
    return lc.link(label    = "Run Simulation",
                   Class    = "epsc-run-task",
                   onclick  = load(actor     ='jobs/submit',
                                  routine   = 'submit',
                                  id        = id,
                                  taskid    = taskid,
                                  subtype   = "epsc",   # Used to identify job type!
                                  package   = "epsc"))


def jobLink(director, id, taskid):
    "Returns link to job"
    jobs        = director.clerk.getQEJobs(where="taskid='%s'" % taskid)

    if not jobs:
        return "None"

    job  = latestJob(jobs)

    return lc.link(label   = job.id,
                   onclick = load(actor     = 'jobs/jobs-view',
                                  id        = id,
                                  taskid    = taskid,
                                  jobid     = job.id,
                                  type      = "epsc",
                                  package   = "EPSC"))


def allJobsLink(director, id, taskid):
    "Returns link to all jobs"
    return lc.link(label    = "All Jobs",
                   Class    = "qe-all-jobs", # Class = "qe-task-action"
                   onclick = load(actor     = 'jobs/jobs-view-all',
                                  id        = id,
                                  taskid    = taskid,
                                  type      = "epsc",
                                  linkorder = 0,
                                  package   = "EPSC"))



__date__ = "$Mar 23, 2011 7:15:15 PM$"


