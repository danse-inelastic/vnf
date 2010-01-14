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

from vnfb.utils.qeconst import SIMCHAINS
from vnfb.utils.qetaskcell import QETaskCell
from vnfb.utils.qegrid import QEGrid

import luban.content as lc
from luban.content.Splitter import Splitter
from luban.content.Paragraph import Paragraph
from luban.content import load
from luban.content.Link import Link

# TODO:
# - Do not display action buttons "Run Task" or "Cancel" unless previous simulation
#   is running or completed
# - Change action buttom depending on the status of the job:
#   "Run Task" -> "Cancel" -> "Run Task"

class QETasks:
    """Displays the chain of QE simulation steps"""

    def __init__(self, director, type, simid = None):
        self._simid     = simid
        self._director  = director
        self._simtype   = type
        self._simlist   = self._getSimlist(type)


    def tasks(self):
        container   = ""
        if self._simid:
            # At most one task for each simtask is possible
            simtasks        = self._director.clerk.getQESimulationTasks(where="simulationid='%s'" % self._simid)
            taskslist       = self._tasksList(simtasks)

            table           = QEGrid(lc.grid(Class="qe-tasks-table"))
            doshow          = self._showActions(taskslist)  # show "Run Task"?

            for i in range(self._tasknum()):
                rows    = self._list(doshow)
                self._setTaskCell(table, i, taskslist[i], rows)
                if doshow:
                    # Special layout for action buttons (e.g. "Run Task")
                    table.setCellStyle(2, i, "qe-action-task")

            container   = table.grid()
            
        return container


    def _setTaskCell(self, table, colnum, task, rows):
        "Populates the task's cell"

        tc      = QETaskCell(self._director, self._type(colnum), colnum, self._simid, task)
        fields  = [tc.header(), tc.taskInfo(), tc.action()]
        for i in range(len(rows)):
            rows[i] = fields[i]
        table.addColumn(rows)


    def _showActions(self, taskslist):
        doshow  = False
        for t in taskslist:
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

    def _type(self, colnum):
        "Returns task type"
        return self._simlist[colnum]


    def _tasknum(self):
        "Returns number of tasks"
        return len(self._simlist)


    def _tasksList(self, simtasks):
        taskslist   = []
        for type in self._simlist:
            taskslist.append(self._taskObject(simtasks, type))
            
        return taskslist


    def _taskObject(self, simtasks, type):
        """
        Return task object in simtasks of type 'type' or None otherwise
        """
        for st in simtasks:
            if st.taskid != '': # Avoid dangling references
                task    = self._director.clerk.getQETasks(id = st.taskid)
                if task is not None and task.type    == type:
                    return task

        return None


    def _getSimlist(self, type):
        if type in SIMCHAINS:
            return SIMCHAINS[type]

        return ()


if __name__ == "__main__":
    pass


__date__ = "$Nov 9, 2009 10:50:54 AM$"

