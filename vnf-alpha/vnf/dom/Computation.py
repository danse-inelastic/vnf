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


from OwnedObject import OwnedObject as base
class Computation(base):

    # base class for all computations (including simulations)

    import vnf.dom
    results = vnf.dom.referenceSet(name='results')

    import pyre.db
    job = pyre.db.reference(name='job', table = Job)

    results_state = pyre.db.varchar(name='results_state', length=16, default='')
    #  - retrieved
    #  - retrieving
    #  - retrieval failed
    #  - partially retrieved
    #  - (empty)   means nothing done

    # pending internal-tasks to get this computation going
    pending_tasks = vnf.dom.referenceSet(name='pending_tasks')



def findPendingTask(computation, iworker=None, director=None):
    import journal
    debug = journal.debug('itask-findPendingTask')
    
    pending_tasks = computation.pending_tasks.dereference(director.clerk.db)
    if not pending_tasks: return

    found = None
    for label, task in pending_tasks:
            
        # if not the right task, skip
        if task.worker != iworker: continue

        if task.state == 'finished':
            raise RuntimeError, "Task %s for %s finished but apparently it is not giving the right results or the results of this task has been mistakenly removed." % (task.id, computation.id)

        if task.state == 'failed':
            debug.log("Task %s for %s found. Which has failed before." % (task.id, computation.id))
            return 'task failed'

        if task.state == 'cancelled':
            debug.log("Task %s for %s found. Which has been cancelled before." % (task.id, computation.id))
            # reopen the task
            task.state = 'created'
            director.clerk.updateRecord(task)
            found = task
            break

        found = task
        break
    
    return found
    

# version
__id__ = "$Id$"

# End of file 
