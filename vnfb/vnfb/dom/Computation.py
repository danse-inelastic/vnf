# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

'''
Computation is the base class of all kinds of computations.
All computation tables should be inherited from this base class.
It is an abstract class, not a real table.
There are abstract subclasses of Computation, such as MaterialSimulation,
which define special categories of computations.

Class attributes of a computation table inherited from this base class:
  * job_builder: the "job_builder" component for this computation.
    eg. "material_simulations/bvk_getdos"
  * actor: the actor component for this computation
    eg. "material_simulations/bvk_getdos"
'''



from Job import Job


from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base

# base class for all computations (including simulations)
class Computation(base):


    import dsaw.db


    short_description = dsaw.db.varchar(name='short_description', length = 128, default='')
    short_description.meta['tip'] = 'short_description'

    import vnf.dom
    results = dsaw.db.referenceSet(name='results')

    # job = dsaw.db.reference(name='job', table = Job)

    results_state = dsaw.db.varchar(name='results_state', length=16, default='')
    #  - retrieved
    #  - retrieving
    #  - retrieval failed
    #  - partially retrieved
    #  - (empty)   means nothing done

    # pending internal-tasks to get this computation going
    # pending_tasks = vnf.dom.referenceSet(name='pending_tasks')

    
    def getJobs(self, db):
        from Job import Job
        return self.getReferences(db, Job, 'computation')
    def getJob(self, db):
        jobs = self.getJobs(db)
        # here we assume one computation only have one job
        # to get all jobs use method "getJobs"
        if len(jobs)>1: raise RuntimeError
        if not jobs: return None
        return jobs[0]
    

    def findPendingTask(self, db, iworker=None):
        import journal
        debug = journal.debug('itask-findPendingTask')
        from ITask import ITask
        tasks = self.getReferences(db, ITask, 'beneficiary')
        if not tasks: return

        found = None
        for task in tasks:
            
            # if not the right task, skip
            if task.worker != iworker: continue

            if task.state == 'finished':
                raise RuntimeError, "Task %s for %s finished but apparently it is not giving the right results or the results of this task has been mistakenly removed." % (task.id, self.id)

            if task.state == 'failed':
                debug.log("Task %s for %s found. Which has failed before." % (task.id, self.id))
                return task

            if task.state == 'cancelled':
                debug.log("Task %s for %s found. Which was cancelled." % (task.id, self.id))
                # reopen the task
                task.state = 'created'
                db.updateRecord(task)
                found = task
                break

            found = task
            break

        return found


    @classmethod
    def getJobBuilderName(cls):
        if hasattr(cls, 'job_builder'): return cls.job_builder
        return cls.__name__.lower()


    @classmethod
    def getActorName(cls):
        if hasattr(cls, 'actor'): return cls.actor
        return cls.__name__.lower()


# version
__id__ = "$Id$"

# End of file 
