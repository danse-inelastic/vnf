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

from vnfb.utils.qegrid import QEGrid
from vnfb.utils.qeinput import QEInput

class QETaskCell:

    def __init__(self, director, type, simid, task):
        self._type  = type
        self._simid = simid
        self._task  = task
        self._director  = director


    def header(self):
        "Shows the header for the simulation task"
        type    = lc.paragraph(text=self._type, Class="text-bold")
        link    = lc.paragraph(text="")     # Task cannot be changed at this time
        #link    = lc.link(label="Change")  # Keep

        table   = QEGrid(lc.grid(Class="qe-grid"))
        table.addRow((type, link), (None, "qe-task-header-change"))

        return table.grid()


    def taskInfo(self):
        table   = QEGrid(lc.grid(Class="qe-tasks-info"))
        if self._task:
            table.addRow(("Task:", self._taskId()))
            table.addRow(("Input:", self._input()))
            table.addRow(("Output:", self._output()))
            table.addRow(("Status:", self._status()))
            table.addRow(("Job:", self._job()))
            table.setColumnStyle(0, "qe-tasks-param")
            table.setCellStyle(3, 1, "text-green")

            #table.addRow(("Jobs:", self._jobs()))  # Keep
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
        link    = ""
        if self._task:
            link = lc.link(label="Run Task",
                           Class="qe-run-task",
                           onclick = load(actor     ='jobs/submit',    # 'jobs/checksubmit'
                                          routine   = 'submit',        # 'checkSubmit'
                                          id        = self._simid,
                                          taskid    = self._task.id)
                            )

        return link

    def _taskId(self):
        tid = self._task.id
        return lc.link(label    = tid,
                       onclick  = load(actor    = 'material_simulations/espresso/task-view',
                                       id       = self._simid,
                                       taskid   = tid,
                                       type     = self._type)
                        )


    def _input(self):
        # Suppose that self._task is not None
        qeinput = QEInput(self._director, self._simid, self._task.id, self._type)
        return qeinput.getLink()

    def _output(self):
        return "ni.scf.out"

    def _status(self):
        "Displays status of the simulation"
        link    = "Not Started"
        jobs    = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            job  = jobs[0]
            link = job.status

        return link


    def _job(self):
        "Displays id of the current job"
        link    = "None"
        jobs    = self._director.clerk.getQEJobs(where="taskid='%s'" % self._task.id)
        if jobs:
            job  = jobs[0]
            link = lc.link(label=job.id,
                           onclick = load(actor     ='material_simulations/espresso/sim-view',
                                          id        = self._simid)
                            )

        return link

__date__ = "$Dec 12, 2009 3:21:13 PM$"


