# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from vnf.dom.QETask import QETask
from vnf.qeutils.taskcreator import TaskCreator

class EPSCTaskCreator(TaskCreator):

    def _createTask(self, tasktype, linkorder):
        "Creates task"
        params  = {"type":          tasktype,
                   "package":       "EPSC",
                   "linkorder":     linkorder
                   }
        task     = QETask(self._director)
        task.createRecord(params)
        self._taskid    = task.id


__date__ = "$Mar 23, 2011 3:35:40 PM$"


