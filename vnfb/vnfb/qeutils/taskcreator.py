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

from vnfb.qeutils.qeutils import simchain
from vnfb.dom.QETask import QETask
from vnfb.dom.QESimulationTask import QESimulationTask

class TaskCreator:
    "Creates a single task record (touches other records is needed)"
    
    def __init__(self, director, simid):
        self._director  = director
        self._simid     = simid
        self._taskid    = ""


    def createMissingRecords(self, chain):
        "Create non existing records for some simulation"
        # Example of input: "electron-min,ion-min"
        tasktypes   = simchain(chain)
        for i in range(len(tasktypes)):
            self.createRecord(tasktypes[i], i)


    def createRecord(self, tasktype, linkorder):
        "Create simulation record"
        print tasktype
#        self._createTask(tasktype, linkorder)
#        self._referenceSimulationTask()


    def _createTask(self, tasktype, linkorder):
        "Creates task"
        params  = {"type":          tasktype,
                   "package":       "Quantum Espresso",
                   "linkorder":     linkorder
                   #"matter":        self.matter    # Doesn't work at this moment
                   }
        task     = QETask(self._director)
        task.createRecord(params)
        self._taskid    = task.id


    def _referenceSimulationTask(self):
        """Creates simulation task
        If dangling record (QESimulationTask with the same simulation id and taskid = '')
        already exists - USE IT
        """
        simtask = self._getDanglingReference()

        if simtask:     # dereference (attach to dangling record)
            self._updateSimulationTask(simtask)
            return

        # There are no dangling records
        self._createSimulationTask()


    def _getDanglingReference(self):
        """Get QESimulationTask that has taskid = ''. Make sure that there are no side effects, like
        stored results
        """
        simtasks    = self._director.clerk.getQESimulationTasks(where="simulationid='%s'" % self._simid)
        if simtasks:
            simtask     = simtasks[0]   # Pick the first one
            if simtask.taskid == '':    # Reference is dangling
                return simtask

        return None


    def _updateSimulationTask(self, simtask):
        params  = {"taskid":        self._taskid, }
        simtask.setDirector(self._director)
        simtask.updateRecord(params)


    def _createSimulationTask(self):
        "Creates new QESimulationTask"
        params  = {"simulationid":  self._simid,
                   "taskid":        self._taskid
                  }
        simtask = QESimulationTask(self._director)
        simtask.createRecord(params)


#    def _taskType(self):
#        "Returns task type"
#        if self._simchain == "":
#            return self._type
#
#        list    = self._simchain.split(",")
#        if self._linkorder in range(len(list)):
#            return list[self._linkorder]
#
#        return self._type
#

__date__ = "$May 14, 2010 7:06:17 PM$"


