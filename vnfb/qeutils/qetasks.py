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

from vnfb.qeutils.taskcell import TaskCell
from vnfb.qeutils.qegrid import QEGrid
from vnfb.qeutils.qerecords import SimulationRecord

import luban.content as lc

# TODO:
# - Do not display action buttons "Run Task" or "Cancel" unless previous simulation
#   is running or completed
# - Change action buttom depending on the status of the job:
#   "Run Task" -> "Cancel" -> "Run Task"

class QETasks:
    """Displays the chain of QE simulation steps"""

    def __init__(self, director, simid, simtype, simchain):
        self._director  = director
        self._simid     = simid
        self._simtype   = simtype
        self._simchain  = simchain


    def tasks(self):
        container   = ""

        simrecord   = SimulationRecord(self._director, self._simid)
        tasklist    = simrecord.taskList()

        if not tasklist:
            return container

        self._types     = simrecord.typeList()
        table           = QEGrid(lc.grid(Class="qe-tasks-table"))
        doshow          = self._showActions(tasklist)  # show "Run Task"?

        for i in range(len(tasklist)):
            rows    = self._list(doshow)
            self._setTaskCell(table, i, tasklist[i], rows)
            if doshow:
                # Special layout for action buttons (e.g. "Run Task")
                table.setCellStyle(2, i, "qe-action-task")

        return table.grid()


    def _setTaskCell(self, table, linkorder, task, rows):
        "Populates the task's cell"

        tc      = TaskCell(self._director, self._types[linkorder], linkorder, self._simid, task)
        fields  = [tc.header(), tc.taskInfo(), tc.action()]

        for i in range(len(rows)):
            rows[i] = fields[i]
        table.addColumn(rows)


    def _showActions(self, tasklist):
        doshow  = False
        for t in tasklist:
            if t:
                doshow = True

        return doshow


    def _list(self, doshow):
        """Return list of size 'num' filled with None values
        If at least one task is created show 3 rows, else show 2 rows
        """
        num     = 2
        if doshow:
            num = 3

        return [None for i in range(num)]


    def _type(self, linkorder):
        "Returns task type"
        return self._simlist[linkorder]


if __name__ == "__main__":
    pass


__date__ = "$Nov 9, 2009 10:50:54 AM$"

