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

class QETaskCell:

    def __init__(self, type):   # Temp
        self._type  = type

    def header(self):
        "Shows the header for the simulation task"
        type    = lc.paragraph(text=self._type, Class="text-bold")
        link    = lc.link(label="Change")

        table   = QEGrid(lc.grid(Class="qe-grid"))
        table.addRow((type, link), (None, "qe-task-header-change"))

        return table.grid()


    def taskInfo(self):
        table   = QEGrid(lc.grid(Class="qe-tasks-info"))

#        self._addCell(table, "Create New Task")
#        self._addCell(table, "or")
#        self._addCell(table, "Use Existing Task")
        
        table.addRow(("Task:", self._taskId()))
        table.addRow(("Input:", self._input()))
        table.addRow(("Output:", self._output()))
        table.addRow(("Status:", self._status()))
        table.addRow(("Job:", self._currentJob()))
        
        #table.addRow(("Jobs:", self._jobs()))
        
        table.setColumnStyle(0, "qe-tasks-param")
        table.setCellStyle(3, 1, "text-green")

        return table.grid()

    def action(self):
        return lc.link(label="Run Task",
                       Class="qe-run-task",
                       onclick = load(actor='material_simulations/espresso/sim-edit')
                        )


    def _taskId(self):
        return "VBDG4"

    def _input(self):
        return "ni.scf.in"

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


