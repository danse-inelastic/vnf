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
            table.addRow(("Job:", self._currentJob()))
            table.setColumnStyle(0, "qe-tasks-param")
            table.setCellStyle(3, 1, "text-green")

            #table.addRow(("Jobs:", self._jobs()))
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
        return lc.link(label="Run Task",
                       Class="qe-run-task",
                       onclick = load(actor='material_simulations/espresso/sim-edit')
                        )


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
        qeinput = QEInput(self._director, self._task.id, self._type) 
        return qeinput.getLink()

    def _output(self):
        return "ni.scf.out"

    def _status(self):
        return "Running"

    def _currentJob(self):
        return "RBGF6"

    def _jobs(self):
        return "RBGF6, BNFGS"


#    def _addCell(self, table, value):
#        row     = table.row()
#        cell    = row.cell()
#        cell.add(value)


#        link        = Link(label="Add",
#                           onclick=load(actor      = "material_simulations/espresso/input-add",
#                                        id         = id,
#                                        type       = self._simlist[colnum])
#                          )

__date__ = "$Dec 12, 2009 3:21:13 PM$"


