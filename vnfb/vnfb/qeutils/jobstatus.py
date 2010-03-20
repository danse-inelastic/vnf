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

"""
Displays the status of the job
"""

from vnfb.qeutils.qerecords import SimulationRecord

import luban.content as lc
from luban.content import load

ID_OUTPUT       = "qe-container-output"
ID_STATUS       = "qe-container-status"

DEFAULT_MESSAGE = "Not Started"

class JobStatus(object):

    def __init__(self, director, simid, type):
        self._director  = director
        self._simid     = simid
        self._type      = type
        self._job       = None
        self._task      = None

        self._init()


    def _init(self):
        simrecord   = SimulationRecord(self._director, self._simid)
        if not simrecord:
            return

        self._job   = simrecord.job(self._type)
        self._task  = simrecord.task(self._type)


    def message(self):
        "Returns status message"
        doc     = lc.document(id = ID_STATUS)
        content = lc.htmldocument(text = DEFAULT_MESSAGE)
        doc.add(content)

        if not self._job:
            return doc
        
        content.text    = self._job.status
        return doc


    def action(self):
        "Return action link"
        if not self._job or not self._task:
            return ""

        return lc.link(label="Refresh",
                      Class     = "qe-task-action",
                      onclick   = load(actor     = 'jobs/status',
                                       routine   = 'retrieveStatus',
                                      id        = self._simid,
                                      taskid    = self._task.id,
                                      jobid     = self._job.id)
                     )


    def output(self):
        doc     = lc.document(id=ID_OUTPUT)
        doc.add("None")
        return doc


__date__ = "$Mar 18, 2010 11:05:41 PM$"

