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


from Job import Job


from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base
class Computation(base):

    # base class for all computations (including simulations)

    import vnf.dom
    results = vnf.dom.referenceSet(name='results')

    import dsaw.db
    # job = dsaw.db.reference(name='job', table = Job)

    results_state = dsaw.db.varchar(name='results_state', length=16, default='')
    #  - retrieved
    #  - retrieving
    #  - retrieval failed
    #  - partially retrieved
    #  - (empty)   means nothing done

    # pending internal-tasks to get this computation going
    # pending_tasks = vnf.dom.referenceSet(name='pending_tasks')

    def getJob(self, db):
        from Job import Job
        jobs = self.getReferences(db, Job, 'computation')
        # right now we assume one computation only have one job
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
    

# version
__id__ = "$Id$"

# End of file 
