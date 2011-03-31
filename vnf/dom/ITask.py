# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from OwnedObject import OwnedObject as base
class ITask(base):

    'internal tasks'

    name = 'itasks'

    import dsaw.db
    
    time_completion = dsaw.db.timestamp(name='time_completion')
    time_completion.meta['tip'] = 'time left to completion'
    
    time_start = dsaw.db.timestamp(name='time_start')
    time_start.meta['tip'] = 'the time the job started'
    
    state = dsaw.db.varchar( name = 'state', length = 16 )
    # state:
    #   - created: just created. has not been submitted
    #   - running
    #   - finished
    #   - failed
    #   - cancelled
    
    progress_percentage = dsaw.db.real(name='progress_percentage')
    progress_text = dsaw.db.varchar(name='progress_text', length=1024)

    # the party that benefits from this internal task
    beneficiary = dsaw.db.versatileReference(
        name = 'beneficiary')
    
    # the type of this internal task
    type = dsaw.db.varchar(name='type', length=128)

    # the worker of this internal task
    worker = dsaw.db.varchar(name='worker', length=128)
    
    options = dsaw.db.varcharArray(name='options', length=64, default=[])

    error = dsaw.db.varchar(name='error', length=8192)



# interface for db tables that have tasks
class HasTask(object):

    
    def getOnlyTask(self, db, iworker=None):
        "get the only itask for the given iworker. if none found, return none"
        from ITask import ITask
        tasks = self.getReferences(db, ITask, 'beneficiary')
        tasks = [t for t in tasks if t.worker == iworker]
        if len(tasks) > 1:
            # XXX should be integrity error
            raise RuntimeError, "more than 1 tasks found for retrieving results: %s" % (
                [t.id for t in tasks], )
        if not tasks: return
        return tasks[0]




def createITask(id, beneficiary, worker, type='', state='created', **options):
    t = ITask()
    t.id = id
    t.beneficiary = beneficiary
    t.worker = worker
    opts = []
    for k, v in options.iteritems():
        opts.append(str(k))
        opts.append(str(v))
        continue
    t.options = opts
    t.type = type
    t.state = state
    t.progress_percentage = 0
    return t


# version
__id__ = "$Id$"

# End of file 
