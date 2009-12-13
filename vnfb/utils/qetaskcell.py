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

class QETaskCell:

    def __init__(self, type):   # Temp
        self._type  = type

    def header(self):
        "Shows the header for the simulation task"
        type    = lc.paragraph(text=self._type, Class="text-bold")
        link    = lc.link(label="Change")

        table   = lc.grid(Class="qe-grid")
        row     = table.row()
        cell    = row.cell()
        cell.add(type)
        # Add link only if id is not None
        cell    = row.cell(Class="qe-task-header-change")
        cell.add(link)
        
        return table


    def taskInfo(self):
        table   = lc.grid(Class="qe-tasks-info")

        self._addCell(table, "Create New Task")
        self._addCell(table, "or")
        self._addCell(table, "Use Existing Task")
        
#        self._addRow(table, "Task:", self._taskId(), ("qe-tasks-param", ""))
#        self._addRow(table, "Input:", self._input(), ("qe-tasks-param", ""))
#        self._addRow(table, "Output:", self._output(), ("qe-tasks-param", ""))
#        self._addRow(table, "Status:", self._status(), ("qe-tasks-param", "text-green"))
#        self._addRow(table, "Job:", self._currentJob(), ("qe-tasks-param", ""))
        
        #self._addRow(table, "Jobs:", self._jobs())

        return table

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


    def _addRow(self, table, param, value, tdclass = None):
        """Add row with two columns
        tdclass - tuple of classes applied to the cell
        """
        def cellfactory(row, tdclass, colnum):
            if tdclass:
                return row.cell(Class=tdclass[colnum])

            return row.cell()
        
        row     = table.row()
        cell    = cellfactory(row, tdclass, 0)
        cell.add(param)
        cell    = cellfactory(row, tdclass, 1)
        cell.add(value)


    def _addCell(self, table, value):
        row     = table.row()
        cell    = row.cell()
        cell.add(value)


#        link        = Link(label="Add",
#                           onclick=load(actor      = "material_simulations/espresso/input-add",
#                                        id         = id,
#                                        type       = self._simlist[colnum])
#                          )

__date__ = "$Dec 12, 2009 3:21:13 PM$"


