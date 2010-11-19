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

import luban.content as lc
from luban.content import load
from vnfb.qeutils.qeutils import jobStatus


class TaskAction(object):
    """
    TaskAction - class that return task action link ("Run Task", "Cancel", "No Connection")
    """
    def __init__(self, director, simid, job, task):
        self._director  = director
        self._simid     = simid
        self._job       = job
        self._task      = task


    # Temp solution to speed up sim-view load
#    def link(self):
#        if not self._director or not self._task:
#            return "None"
#
#        return self._runLink()

 
    # Rename to link()
    def link(self): #linkUpdated(self):
        if not self._director or not self._task:
            return "None"

        if self._job:
            server  = self._director.clerk.getServers(id = self._job.serverid)
            status  = jobStatus(self._director, self._job, server)

            # Still can through an exception
            if status and type(status["state"]) == str and status["state"].lower() != "finished":
                return self._cancelLink()

        return self._runLink()


    def _runLink(self):
        "Returns 'Run Task' link"
        # If not job created or is not running
        link = lc.link(label    = "Run Task",
                       Class    = "qe-run-task",
                       onclick  = load(actor     ='jobs/submit',    # 'jobs/checksubmit'
                                      routine   = 'submit',
                                      id        = self._simid,
                                      taskid    = self._task.id,
                                      subtype   = self._task.subtype,
                                      optlevel  = self._optlevel())
                        )
        return link


    def _optlevel(self):
        "Returns optlevel from qesettings"
        settingslist    = self._director.clerk.getQESettings(where="simulationid = '%s'" % self._simid)
        if not settingslist:
            return "0"

        settings = settingslist[0]
        return str(settings.optlevel)


    def _cancelLink(self):
        "Returns 'Cancel' link"
        link = lc.link(label    = "Cancel",
                       Class    = "qe-cancel-task",
                       onclick  = load(actor    ='jobs/cancel',
                                      routine   = 'cancel',
                                      simid     = self._simid,
                                      jobid     = self._job.id,
                                      taskid    = self._task.id)
                        )
        return link



__date__ = "$Apr 19, 2010 9:53:34 AM$"


