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

from vnfb.dom.QETask import QETask
from vnfb.dom.QESimulationTask import QESimulationTask

class TaskCreator:
    "Creates a single task record (touches other records is needed)"
    
    def __init__(self, director, simid):
        self._director  = director
        self._simid     = simid

    #self._simchain  = simchain  # Example: "electron-min,ion-min"

    def createRecord(self):
        "Create simulation record"
        self._createTask(director)
        self._referenceSimulationTask(director)


    def createMissingRecords(self):
        "Create non existing records for some simulation"


    def _createTask(self, director):
        "Creates task"
        params  = {"type":          self.tasktype,
                   "package":       "Quantum Espresso",
                   "linkorder":     self.linkorder
                   #"matter":        self.matter    # Doesn't work at this moment
                   }
        task     = QETask(director)
        task.createRecord(params)
        self._taskid    = task.id


    def _referenceSimulationTask(self, director):
        """Creates simulation task
        If dangling record (QESimulationTask with the same simulation id and taskid = '')
        already exists - USE IT
        """
        simtask = self._getDanglingReference(director)

        if simtask:     # Dereference (attach to dangling record)
            self._updateSimulationTask(director, simtask)
            return

        # There are no dangling records
        self._createSimulationTask(director)


    def _getDanglingReference(self, director):
        """Get QESimulationTask that has taskid = ''. Make sure that there are no side effects, like
        stored results
        """
        simtasks    = director.clerk.getQESimulationTasks(where="simulationid='%s'" % self.simid)
        if simtasks:
            simtask     = simtasks[0]   # Pick the first one
            if simtask.taskid == '':    # Reference is dangling
                return simtask

        return None


    def _updateSimulationTask(self, director, simtask):
        params  = {"taskid":        self._taskid, }
        simtask.setDirector(director)
        simtask.updateRecord(params)


    def _createSimulationTask(self, director):
        "Creates new QESimulationTask"
        params  = {"simulationid":  self.simid,
                   "taskid":        self._taskid
                  }
        simtask = QESimulationTask(director)
        simtask.createRecord(params)


    def _taskType(self):
        "Returns task type"
        if self._simchain == "":
            return self._type

        list    = self._simchain.split(",")
        if self._linkorder in range(len(list)):
            return list[self._linkorder]

        return self._type


__date__ = "$May 14, 2010 7:06:17 PM$"


