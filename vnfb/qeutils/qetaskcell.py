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

import os
import luban.content as lc
from luban.content import load, select

from vnfb.qeutils.qeresults import QEResults
from vnfb.qeutils.qegrid import QEGrid
from vnfb.qeutils.qeinput import QEInput
from vnfb.qeutils.qetaskinfo import TaskInfo
from vnfb.qeutils.qeutils import latestJob

RUN_TASK    = "run-task"

class QETaskCell:

    def __init__(self, director, type, colnum, simid, task):
        self._type      = type
        self._simid     = simid
        self._task      = task
        self._colnum    = colnum
        self._job       = None
        self._director  = director


    def header(self):
        "Shows the header for the simulation task"
        type    = lc.paragraph(text="Step %s: %s" % (self._colnum+1 , self._type), Class="text-bold")
        link    = lc.paragraph(text="")     # Task cannot be changed at this time
        #link    = lc.link(label="Change")  # Keep

        table   = QEGrid(lc.grid(Class="qe-grid"))
        table.addRow((type, link), (None, "qe-task-header-change"))

        return table.grid()


    def taskInfo(self):
        table   = QEGrid(lc.grid(Class="qe-tasks-info"))
        if self._task:
            self._taskId(table)
            self._input(table)
            self._status(table)
            self._output(table)
            self._jobId(table)
            self._results(table)

            table.setColumnStyle(0, "qe-tasks-param")
            table.setColumnStyle(1, "qe-tasks-value")

            table.setCellStyle(3, 1, "text-green")
        else:
            # May be it would be better to just replace content with task info?
            link    = lc.link(label="Create New Task",
                              onclick = load(actor      = 'material_simulations/espresso/task-create',
                                             routine    = 'createRecord',
                                             simid      = self._simid,
                                             tasktype   = self._type)
                             )

            table.addRow((link, ))   
            #table.addRow(("or", ))                 # Keep
            #table.addRow(("Use Existing Task", ))  # Keep

        return table.grid()


    def action(self):
        "Displays simulation task action button: 'Run Task', 'Cancel'"
        doc     = lc.document()   # Example: run-task-BFDFX56
        link    = ""
        if self._task:
            link = lc.link(label    = "Run Task",
                           Class    = "qe-run-task",
                           onclick  = load(actor     ='jobs/submit',    # 'jobs/checksubmit'
                                          #routine   = 'submitProgress',        # 'checkSubmit'
                                          routine   = 'submit',
                                          id        = self._simid,
                                          taskid    = self._task.id,
                                          subtype   = self._task.short_description)
                            )
            doc.id = "run-task-%s" % self._task.id

        doc.add(link)
        return doc


    def _taskId(self, table):
        tid     = self._task.id
        link    = lc.link(label    = tid,
                           onclick  = load(actor    = 'material_simulations/espresso/task-view',
                                           id       = self._simid,
                                           taskid   = tid,
                                           type     = self._type)
                            )

        table.addRow(("Task:", link, ""))


    def _input(self, table):
        # Suppose that self._task is not None
        qeinput = QEInput(self._director, self._simid, self._task.id, self._type)
        table.addRow(("Input:", qeinput.getLink(), ""))


    def _output(self, table):
        table.addRow(("Output:", "None", ""))


    def _status(self, table):
        "Displays status of the simulation"
        action  = ""
        link    = "Not Started"
        jobs    = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            job  = latestJob(jobs)
            action  = lc.link(label="Refresh",
                              Class     = "qe-task-action",
                              onclick   = load(actor     = 'jobs/status',
                                               routine   = 'retrieveStatus',
                                              id        = self._simid,
                                              taskid    = self._task.id,
                                              jobid     = job.id)  #,type      = self._type
                             )

            link = job.status

        
        table.addRow(("Status:", link, action)) # Replace: Status -> Job Status


    def _jobId(self, table):
        "Displays id of the current job" 
        link        = "None"  
        action      = ""
        jobs        = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            self._job  = latestJob(jobs)
            link = lc.link(label=self._job.id,
                               onclick = load(actor     = 'jobs/jobs-view',
                                              id        = self._simid,
                                              taskid    = self._task.id,
                                              jobid     = self._job.id,
                                              type      = self._type)
                                )
            action = lc.link(label    = "All Jobs",
                              Class    = "qe-all-jobs", # Class = "qe-task-action"
                               onclick = load(actor     = 'jobs/jobs-view-all',
                                              id        = self._simid,
                                              taskid    = self._task.id,
                                              type      = self._type)
                                )

        table.addRow(("Job:", link, action))


    def _results(self, table):
        "Returns link to tar file for download. "
        taskinfo    = TaskInfo(self._simid, self._task.id, self._type)
        results     = QEResults(self._director, self._job, taskinfo)
        container   = results.link()
        action      = results.action()
        
        table.addRow(("Results: ", container, action))


__date__ = "$Dec 12, 2009 3:21:13 PM$"


