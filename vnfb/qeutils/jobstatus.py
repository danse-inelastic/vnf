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
from vnfb.qeutils.message import Message
from vnfb.qeutils.qeconst import ID_OUTPUT, ID_STATUS
from vnfb.qeutils.qeutils import key2str
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

        if not self._input or not self._task:     # No input record, no output can be found
            content.add(NONE)
            return doc

        localpath   = "../content/data/tmp" # Let's store output file to tmp/ directory
        file        = "%s%s.in.out" % (self._input.id, self._task.type.lower())
        outputfile  = os.path.join(localpath, file)

        if not os.path.exists(outputfile):    # No output file
            content.add(NONE)
            return doc

        # XXX: It will show output for current input only! When you delete input 
        # record no output is displayed

        dialog = lc.dialog(title='Output for %s' % self._input.id, autoopen=True, Class="qe-dialog-output")
        dialog.paragraph(text=open(outputfile).read())  # Text
        okbutton = lc.button( label     = 'OK',
                              onclick   = select(element=dialog).destroy())
        dialog.add(okbutton)
        link    = lc.link(label     = 'Output',
                          onclick   = select(element=content).append(dialog))  #id = self._outputId()

        content.add(link)
        
# Keep code!
#
#        parts       = localpath.split("../content/data/")
#        outputpath  = os.path.join(parts[1], file)
#
#        status  = Message()
#        status.setHtmlLink(file, outputpath)
#
#        content.add(status.string("a"))

        return doc


    def _statusId(self):
        return "%s-%s" % (ID_STATUS, self._linkorder)


    def _outputId(self):
        return "%s-%s" % (ID_OUTPUT, self._linkorder)

__date__ = "$Mar 18, 2010 11:05:41 PM$"


