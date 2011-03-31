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

from vnf.qeutils.qeutils import latestJob, simChain
from vnf.qeutils.qeconst import SIMCHAINS
from vnf.epscutils.epscconst import EPSCCHAIN

class QERecords(object):

    def __init__(self, director):
        # Define interface attributes
        self._director  = director
        self._joblist   = []      # job
        self._tasklist  = []      # task
        self._inputlist = []      # input
        self._jitlist   = []      # job-input-task


# XXX: BAD to pass subtype. But it is a simple way improve load page time!
class SimulationRecord(QERecords):
    "Retrieves records related to various qe database tables: QESimulation, "

    def __init__(self, director, id, subtype = None):
        super(SimulationRecord, self).__init__(director)

        # Additional attributes
        self._id        = id        # simulation id
        self._subtype   = subtype   # EVIL
        self._sim       = None      # simulation object
        self._simtasks  = []        # simulation-task
        self._typelist  = []        # simulation tasks type list

        self._init()


    def _init(self):
        """Init class attributes
        Notes:
            - It is important to set _typelist and _tasklist attributes
        """
        if not self._director:  # No director, no init
            return

        # Should be set before typelist and tasklist
        self._sim       = self.record()
        self._simtype   = self.simType()
        self._simtasks  = self.simTaskList()

        # Shoud be set before inputlist and joblist!
        self._typelist  = self.typeList()           # Important! List of types
        self._tasklist  = self.taskList()           # Important! List of task objects,
                                                    
        self._joblist   = self.jobList(self._subtype)            # Latest jobs
        self._inputlist = self.inputList()
        self._jitlist   = self.jobInputTaskList(self._subtype)   # Default Jobs-Input - Task list
        

    def record(self):
        "Return simulation object specified by id"
        return self._director.clerk.getQESimulations(id=self._id)   #  can be None
        

    def simTaskList(self):
        return self._director.clerk.getQESimulationTasks(where="simulationid='%s'" % self._id) #  can be None


    def simType(self):
        "Return simulation type"
        if not self._sim:
            return None         # No simulation

        simtype     = self._sim.type

        #        if simtype in SIMCHAINS:
        #            return simtype
        #
        #        return None

        # Return plane simtype
        return simtype



    # XXX: Get type list from qesimulations.simchain record, instead of SIMCHAINS
    def typeList(self):
        "Return list of simulation task types"
        if not self._sim:
            return None             # No simulation

        # XXX: Fix reference to the actual simulation type
        if self._simtype == "Molecular Dynamics": # Special case for molecular dynamics
            return simChain(self._sim.simchain)

        if self._simtype in SIMCHAINS.keys():   # QE
            return SIMCHAINS[self._simtype]

        if self._simtype in EPSCCHAIN.keys():   # EPSC
            return EPSCCHAIN[self._simtype]

        return ()


    def taskList(self):
        "Return list of task objects from list of simulation task objects"
        tasklist   = []
        for lo in range(len(self._typelist)):   # Loop over linkorder's
            tasklist.append(self._taskLinkObject(lo))   # Important line

        return tasklist


    def jobList(self, subtype = None):
        "Return list of job objects from list of task objects"
        joblist    = []
        for t in self._tasklist:
            joblist.append(self._jobObject(t, subtype))

        return joblist


    def inputList(self):
        "Return list of input objects from list of task objects"
        inputlist    = []
        for t in self._tasklist:
            inputlist.append(self._inputObject(t))

        return inputlist




    # subtype is not very useful here
    def jobInputTaskList(self, subtype = None):
        return zip(self._joblist, self._inputlist, self._tasklist)


    # subtype is not very useful here
    def jobInputTask(self, linkorder, subtype = None):
        "Returns Job-Input-Task tuple specified by linkorder"
        self._jitlist   = self.jobInputTaskList(subtype)    # set jitlist according to subtype
        for jit in self._jitlist:
            task    = jit[2]

            # Important: linkorder is integer!
            if task and task.linkorder == linkorder:    
                return jit

        return (None, None, None)


    def job(self, linkorder, subtype = None):
        "Convenience method for getting job record specified by linkorder"
        jit = self.jobInputTask(linkorder, subtype)
        return jit[0]


    def input(self, linkorder):
        "Convenience method for getting input record specified by linkorder"
        jit = self.jobInputTask(linkorder)
        return jit[1]


    def task(self, linkorder):
        "Convenience method for getting task record specified by linkorder"
        jit = self.jobInputTask(linkorder)
        return jit[2]


    # For some reason it calls _jobObject too often. Performance degradation?
    # Object methods
    def _jobObject(self, task, subtype = None):
        "Return *latest* job object from related task object"
        if not task:
            return None

        where   = "taskid='%s'" % task.id
        # *Hack* - storing subtype for the job in 'description' column
        if subtype:
            where   = "%s AND description='%s'" % (where, subtype)

        jobs    = self._director.clerk.getQEJobs(where=where)
        if not jobs:
            return None

        return latestJob(jobs)


    def _inputObject(self, task):
        "Return *first* input object from related task object"
        if not task:
            return None

        inputs    = self._director.clerk.getQEConfigurations(where="taskid='%s'" % task.id)
        if inputs and inputs[0]:    # Pick the first
            return inputs[0]

        return None     # No input related to the task


#    # Not very useful. Depricate?
#    def _taskObject(self, type):
#        "Return task object in simtasks of type 'type' or None otherwise"
#        for st in self._simtasks:
#            if st.taskid == '': # Avoid dangling references
#                continue
#            task    = self._director.clerk.getQETasks(id = st.taskid)
#            if task and task.type == type:
#                return task
#
#        return None


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


