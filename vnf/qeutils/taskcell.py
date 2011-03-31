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
from vnf.qeutils.jobstatus import JobStatus
from vnf.qeutils.results.resultinfo import ResultInfo
from vnf.qeutils.qegrid import QEGrid
from vnf.qeutils.inputinfo import InputInfo
from vnf.qeutils.qeconst import TASK_ACTION, MDLABEL, TYPETIP
from vnf.qeutils.qeutils import latestJob
from vnf.qeutils.taskaction import TaskAction

#from vnf.qeutils.qeutils import jobStatus
#RUN_TASK    = "run-task"
#from vnf.qeutils.taskinfo import TaskInfo
#CLASS_ERROR = 'qe-text-red'
#CLASS_OK    = 'qe-text-blue'
#CLASS_NA    = 'qe-text-black'


class TaskCell:

    def __init__(self, director, type, linkorder, simid, task):
        self._type      = type
        self._simid     = simid
        self._task      = task
        self._linkorder = linkorder
        self._job       = None
        self._director  = director


    def header(self):
        "Shows the header for the simulation task"
        # Because "tip" attribute is not implemented for any text widget (luban limitation)
        # I will choose link widget instead
        type        = lc.link(Class="link-text-hack text-blue text-bold")
        type.label  = "Step %s: %s" % (self._linkorder+1 , self._taskLabel())
        type.tip    = self._taskTip()
        return type

        # KEEP: Changes task
        #link    = lc.paragraph(text="")     # Task cannot be changed at this time
        #link    = lc.link(label="Change")  
        #table   = QEGrid(lc.grid(Class="qe-grid"))
        #table.addRow((type, link), (None, "qe-task-header-change"))
        #table.grid()


    def _taskLabel(self):
        if self._type in MDLABEL.keys():
            return MDLABEL[self._type][0]

        return self._type   # No special label


    def _taskTip(self):
        if self._type in MDLABEL.keys():
            return MDLABEL[self._type][1]

        if self._type in TYPETIP.keys():
            return TYPETIP[self._type]
        
        return self._type   # No special tip


    def taskInfo(self):
        table   = QEGrid(lc.grid(Class="qe-tasks-info"))
        
        if self._task:  # If task exists
            self._setTaskInfo(table)    # Main scenario
            return table.grid()


        # No task created, show link "Create New Task"
        link    = lc.link(label="Create New Task",
                          onclick = load(actor      = 'material_simulations/espresso/task-create',
                                         routine    = 'createRecord',
                                         simid      = self._simid,
                                         tasktype   = self._type,
                                         linkorder  = self._linkorder)
                         )

        table.addRow((link, ))
        #table.addRow(("or", ))                 # Keep
        #table.addRow(("Use Existing Task", ))  # Keep
        return table.grid()


    def action(self):
        "Displays simulation task action button: 'Run Task', 'Cancel'"
        doc     = lc.document()   # Example: run-task-BFDFX56

        if not self._task:
            return doc

        doc.id = "%s-%s" % (TASK_ACTION, self._task.id)
        action  = TaskAction(self._director, self._simid, self._job, self._task)

        doc.add(action.link())
        return doc


    def _setTaskInfo(self, table):
        "Set fields for the task info"
        self._taskId(table)
        self._input(table)
        self._status(table)
        self._jobId(table)
        self._results(table)

        self._setStyle(table)   # beautify table :)
        

    def _taskId(self, table):
        tid     = self._task.id
        link    = lc.link(label    = tid,
                           onclick  = load(actor     = 'material_simulations/espresso/task-view',
                                           id        = self._simid,
                                           taskid    = tid,
                                           type      = self._type,
                                           linkorder = self._linkorder)
                            )

        table.addRow(("Task:", link, ""))


    def _input(self, table):
        # Suppose that self._task is not None
        qeinput = InputInfo(self._director, self._simid, self._task.id, self._type, self._linkorder)
        table.addRow(("Input:", qeinput.getLink(), ""))


    def _status(self, table):
        "Displays status of the simulation and output file"
        jobstatus      = JobStatus(self._director, self._simid, self._linkorder)

        table.addRow(("Status:", jobstatus.status(), jobstatus.action()))
        table.addRow(("Output:", jobstatus.output(), ""))


    def _jobId(self, table):
        "Displays id of the current job" 
        jobs        = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)

        if not jobs:
            table.addRow(("Job:", "None", ""))
            return


        self._job  = latestJob(jobs)

        link = lc.link(label   = self._job.id,
                       onclick = load(actor     = 'jobs/jobs-view',
                                      id        = self._simid,
                                      taskid    = self._task.id,
                                      jobid     = self._job.id,
                                      type      = self._type,
                                      package   = "Quantum Espresso"))
        action = lc.link(label    = "All Jobs",
                          Class    = "qe-all-jobs", # Class = "qe-task-action"
                           onclick = load(actor     = 'jobs/jobs-view-all',
                                          id        = self._simid,
                                          taskid    = self._task.id,
                                          type      = self._type,
                                          linkorder = self._linkorder,
                                          package   = "Quantum Espresso"))

        table.addRow(("Job:", link, action))


    def _results(self, table):
        "Returns link to tar file for download. "
        results     = ResultInfo(self._director, self._simid, self._linkorder)
        
        table.addRow(("Results: ", results.link(), results.action() ))


    def _setStyle(self, table):
        "Set style for the table"
        table.setColumnStyle(0, "qe-tasks-param")
        table.setColumnStyle(1, "qe-tasks-value")
        table.setCellStyle(3, 1, "text-green")


__date__ = "$Dec 12, 2009 3:21:13 PM$"


