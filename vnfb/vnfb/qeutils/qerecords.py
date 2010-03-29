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

from vnfb.qeutils.qeutils import latestJob
from vnfb.qeutils.qeconst import SIMCHAINS


class QERecords(object):

    def __init__(self, director):
        # Define interface attributes
        self._director  = director
        self._joblist   = []      # job
        self._tasklist  = []      # task
        self._inputlist = []      # input
        self._jitlist   = []      # job-input-task


class SimulationRecord(QERecords):
    "Retrieves records related to various qe database tables: QESimulation, "

    def __init__(self, director, id):
        super(SimulationRecord, self).__init__(director)

        # Additional attributes
        self._id        = id        # simulation id
        self._sim       = None      # simulation object
        self._simtasks  = []        # simulation-task
        self._typelist  = []        # simulation tasks type list

        self._init()


    def _init(self):
        "Init class attributes"
        if not self._director:  # No director, no init
            return

        self._sim       = self.record()
        self._simtasks  = self.simTaskList()

        self._typelist  = self.typeList()
        self._simtype   = self.simType()
        self._tasklist  = self.taskList()
        self._joblist   = self.jobList()
        self._inputlist = self.inputList()

        self._jitlist   = self.jobInputTaskList() # Jobs-Input - Task list
        

    def record(self):
        "Return simulation object specified by id"
        return self._director.clerk.getQESimulations(id=self._id)   #  can be None
        

    def simTaskList(self):
        return self._director.clerk.getQESimulationTasks(where="simulationid='%s'" % self._id) #  can be None


    def jobList(self):
        "Return list of job objects from list of task objects"
        joblist    = []
        for t in self._tasklist:
            joblist.append(self._jobObject(t))

        return joblist


    def inputList(self):
        "Return list of input objects from list of task objects"
        inputlist    = []
        for t in self._tasklist:
            inputlist.append(self._inputObject(t))

        return inputlist


    def taskList(self):
        "Return list of task objects from list of simulation task objects"
        tasklist   = []
        for lo in range(len(self._typelist)):   # Loop over linkorder's
            tasklist.append(self._taskLinkObject(lo))   # Important line

        return tasklist


    def jobInputTaskList(self):
        return zip(self._joblist, self._inputlist, self._tasklist)


    def jobInputTask(self, linkorder):
        "Returns Job-Input-Task tuple specified by linkorder"
        for jit in self._jitlist:
            task    = jit[2]
            
            if task and task.linkorder == linkorder:
                return jit

        return None


    def job(self, linkorder):
        "Convenience method for getting job record specified by linkorder"
        jit = self.jobInputTask(linkorder)
        return jit[0]


    def input(self, linkorder):
        "Convenience method for getting input record specified by linkorder"
        jit = self.jobInputTask(linkorder)
        return jit[1]


    def task(self, linkorder):
        "Convenience method for getting task record specified by linkorder"
        jit = self.jobInputTask(linkorder)
        return jit[2]


    def typeList(self):
        "Return list of simulation task types"
        if not self._sim:
            return None             # No simulation

        simtype     = self.simType()
        if simtype:
            return SIMCHAINS[simtype]

        return ()


    def simType(self):
        "Return simulation type"
        if not self._sim:
            return None         # No simulation

        simtype     = self._sim.type
        if simtype in SIMCHAINS:
            return simtype

        return None


    # Object methods
    def _jobObject(self, task):
        "Return *latest* job object from related task object"
        if not task:
            return None

        jobs    = self._director.clerk.getQEJobs(where="taskid='%s'" % task.id)
        if jobs:        
            return latestJob(jobs)  # Pick the latest job

        return None     # No job related to the task


    def _inputObject(self, task):
        "Return *first* input object from related task object"
        if not task:
            return None

        inputs    = self._director.clerk.getQEConfigurations(where="taskid='%s'" % task.id)
        if inputs and inputs[0]:    # Pick the first
            return inputs[0]

        return None     # No input related to the task


    def _taskObject(self, type):
        "Return task object in simtasks of type 'type' or None otherwise"
        for st in self._simtasks:
            if st.taskid == '': # Avoid dangling references
                continue
            task    = self._director.clerk.getQETasks(id = st.taskid)
            if task and task.type == type:
                return task

        return None


    def _taskLinkObject(self, linkorder):
        "Return task object in simtasks specified by 'linkorder' or None otherwise"
        for st in self._simtasks:
            if st.taskid == '': # Avoid dangling references
                continue
            task    = self._director.clerk.getQETasks(id = st.taskid)
            if task and task.linkorder == linkorder:
                return task

        return None


# Add additional classes?
class JobRecord(QERecords):
    pass

class TaskRecord(QERecords):
    pass

class InputRecord(QERecords):
    pass



__date__ = "$Mar 14, 2010 2:55:39 PM$"


