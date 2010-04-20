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

import os
import re
from vnfb.qeutils.message import Message
from vnfb.qeutils.qeconst import ID_OUTPUT, ID_STATUS
from vnfb.qeutils.qeutils import key2str, dataroot
from vnfb.qeutils.qerecords import SimulationRecord

import luban.content as lc
from luban.content import select
from luban.content import load

#ID_OUTPUT       = "qe-container-output"
#ID_STATUS       = "qe-container-status"

NONE    = "None"
DEFAULT_MESSAGE = "Not Started"

class JobStatus(object):

    def __init__(self, director, simid, linkorder):
        self._director  = director
        self._simid     = simid
        self._linkorder = linkorder
        self._job       = None
        self._task      = None
        self._input     = None

        self._init()


    def _init(self):
        simrecord   = SimulationRecord(self._director, self._simid)
        if not simrecord:   # No record, no init
            return

        self._job   = simrecord.job(self._linkorder)
        self._task  = simrecord.task(self._linkorder)
        self._input = simrecord.input(self._linkorder)


    def message(self):
        "Returns status message"
        doc     = lc.document(id = self._statusId())
        content = lc.htmldocument(text = DEFAULT_MESSAGE)
        doc.add(content)

        if not self._job:
            return doc
        
        content.text    = key2str(self._job.status)
        return doc


    def action(self):
        "Return action link"
        if not self._job or not self._task:
            return ""

        return lc.link(label="Refresh",
                      Class     = "qe-task-action",
                      onclick   = load(actor     = 'jobs/status',
                                       routine   = 'refreshStatus',
                                      id        = self._simid,
                                      taskid    = self._task.id,
                                      jobid     = self._job.id,
                                      linkorder = self._linkorder)
                     )

    def output(self):
        doc     = lc.document(id = self._outputId())
        content = lc.document()
        doc.add(content)

        outputfile  = self._outputFile(self._director, self._job)   # Output file

        if not outputfile or not os.path.exists(outputfile):    # No output file
            content.add(NONE)
            return doc

        dialog  = lc.dialog(title='Output for %s task' % self._task.id, autoopen=True, Class="qe-dialog-output")
        text    = lc.htmldocument(text="<pre>%s<pre>" % open(outputfile).read())
        dialog.add(text)   # Text
        okbutton = lc.button( label     = 'OK',
                              onclick   = select(element=dialog).destroy())
        dialog.add(okbutton)
        link    = lc.link(label     = 'Output',
                          onclick   = select(element=content).append(dialog))  #id = self._outputId()

        content.add(link)

        return doc


    # Partially borrowed from actors/jobs/status.odb
    def _outputFile(self, director, job):
        "Returns otuput file"
        if not job:     # No job, no output
            return None

        tmpbase     = os.path.join(dataroot(director, relative=True), "tmp") # Example: ../content/data/tmp
        jobpath     = os.path.join(tmpbase, job.name)   # ../content/data/tmp/qejobs
        jobpath     = os.path.join(jobpath, job.id)     # ../content/data/tmp/qejobs/EXSWTYTK

        if not os.path.exists(jobpath):
            return None

        files       = os.listdir(jobpath)
        file        = self._matchCheck(files)
        return os.path.join(jobpath, file)   # Example: ../content/data/tmp/qejobs/EXSWTYTK/EYWKUYI3q2r.in.out


    # Borrowed from ResultPath class
    # XXX: Fix cardcoded pattern for output file
    def _matchCheck(self, files):
        "Find matching file. Single matching file if possible. Picks first otherwise"
        REEXP   = '[\w]+\.in\.out$'
        for fname in files:
            p   = re.compile(REEXP)
            if p.match(fname):   # matches
                return fname

        return None

    def _statusId(self):
        return "%s-%s" % (ID_STATUS, self._linkorder)


    def _outputId(self):
        return "%s-%s" % (ID_OUTPUT, self._linkorder)

__date__ = "$Mar 18, 2010 11:05:41 PM$"


