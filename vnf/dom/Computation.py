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


from ITask import HasTask
from AbstractOwnedObjectBase import AbstractOwnedObjectBase as base

# base class for all computations (including simulations)
class Computation(HasTask, base):

    import dsaw.db
    
    short_description = dsaw.db.varchar(name='short_description', length = 128, default='')
    short_description.meta['tip'] = 'short_description'

    # XXX: this really should be in the _ComputationResultRetrievals table XXX
    results_state = dsaw.db.varchar(name='results_state', length=16, default='')
    #  - retrieved
    #  - retrieving
    #  - retrieval failed
    #  - partially retrieved
    #  - (empty)   means nothing done
    
    # results is a set of references linking to the computation results
    # In vnf alpha, we also use result.origin to point back from result to computation.
    # In vnf beta, we should not need that back reference, and can just search
    # for the parent computation in the referenceset table. The only penalty is
    # speed and should not be a big problem: looking for the parent computation probably
    # is not very important and will be done only  occasionally.
    # With this "results" set, we can create a generic "results" view
    # easily for all computations.
    results = dsaw.db.referenceSet(name='computation_results')
    
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


    def findTasks(self, db, iworker):
        "find the itasks that are for the given iworker"
        from ITask import ITask
        tasks = self.getReferences(db, ITask, 'beneficiary')
        criteria = lambda x: x.worker == iworker
        return filter(criteria, tasks)
    
    
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
    @classmethod
    def getResultRetrieverName(cls):
        if hasattr(cls, 'result_retriever'): return cls.result_retriever
        return cls.__name__.lower()


    # result retrieval related
    def setResultRetrievalStatusAndErrorMessage(self, status, message, db):
        try:
            self.markResultFileStatusAndErrorMessage(
                filename='', db=db, status=status, message=message)
        except db.InvalidRequestError:
            db.rollback()
            self.markResultFileStatusAndErrorMessage(
                filename='', db=db, status=status, message=message)
        return


    def getResultRetrievalStatus(self, db):
        entry = self.getResultRetrievalEntry(filename='', db=db)
        if entry:
            return entry.status


    def resetResultRetrievalStatus(self, db):
        entry = self.getResultRetrievalEntry(filename='', db=db)
        if entry:
            entry.status = 'failed'
            db.updateRecord(entry)
        return


    def getResultRetrievalErrorMessage(self, db):
        entry = self.getResultRetrievalEntry(filename='', db=db)
        if entry:
            return entry.message


    def isResultFileSaved(self, filename, db):
        status = self.getResultFileStatus(filename, db)
        return status == 'saved'
    

    def getResultFileStatus(self, filename, db):
        entry = self.getResultRetrievalEntry(filename, db=db)
        if entry:
            return entry.status


    def getResultRetrievalEntry(self, filename, db):
        gp = self.globalpointer
        gp = gp and gp.id
        if not gp: return 
        
        where = "computation=%s and filename='%s' "  % (gp, filename)
        rs = db.query(_ComputationResultRetrievals).filter(where).all()
        db.commit()
        
        if not rs: return
        
        if len(rs)>1:
            raise RuntimeError, \
                  "multiple entries in table %s for computation %s(%s), filename %s" % (
                _ComputationResultRetrievals.getTableName(),
                self.getTableName(), self.id,
                filename)
        
        return rs[0]


    def markResultFileAsSaved(self, filename, db):
        self.markResultFileStatusAndErrorMessage(filename, db, 'saved')
        return


    def markResultFileStatusAndErrorMessage(self, filename, db, status, message=None):
        message_len = _ComputationResultRetrievals.message.length
        
        gp = self.globalpointer
        gp = gp and gp.id
        if not gp:
            # no global address yet, means need new entry
            neednewentry = True
        else:
            # look for the entries
            where = "computation=%s and filename='%s'"  % (gp, filename)
            rs = db.query(_ComputationResultRetrievals).filter(where).all()
            db.commit()
            
            if len(rs) == 0:
                # no entry, need one
                neednewentry = True
                
            elif len(rs) > 1:
                # more than one entries, error
                raise RuntimeError, \
                      "multiple entries in table %s for computation %s(%s), filename %s" % (
                    _ComputationResultRetrievals.getTableName(),
                    self.getTableName(), self.id,
                    filename)
                    
            else:
                # found one entry
                neednewentry = False
                r = rs[0]
                
        if neednewentry:
            # create a new entry
            r = _ComputationResultRetrievals()
            r.computation = self
            #db.insertRow(r)
            r.status = status
            #db.updateRecord(r)
            r.filename = filename
            #db.updateRecord(r)
            if message is not None:
                r.message = message[:message_len]
            #db.updateRecord(r)
            db.insertRow(r)
            return

        # update entry
        r.status = status
        if message is not None:
            r.message = message[:message_len]
        db.updateRecord(r)
        return


# method register all computation tables
def registerAllComputationTables(domaccess):
    orm = domaccess.orm
    from computation_types import typenames, deps_typenames
    from dsaw.db.Table import Table as TableBase
    for name in typenames+deps_typenames:
        objectClass = domaccess._getObjectByImportingFromDOM(name)
        if not issubclass(objectClass, TableBase):
            table = orm(objectClass)
        else:
            orm.db.registerTable(table)
        continue
    return


# The table that stores the information about retrievals of results for a computation
# It is in use when retrieving result from the job directory of a computation.
# It keeps track of the status of the file retrieval etc.
from dsaw.db.Table import Table
class _ComputationResultRetrievals(Table):

    name = "_____computation_result_retrievals_____"

    import dsaw.db

    # columns
    id = dsaw.db.integer(name = 'id')
    id.constraints = 'PRIMARY KEY'

    computation = dsaw.db.versatileReference(name='computation')

    # name of the computation result file. if empty, it means this entry is about
    # the retrieval of this computation result as a whole, not about a particular
    # file.
    filename = dsaw.db.varchar(name='filename', length=512)

    # status of the file
    status = dsaw.db.varchar(name='status', length=32)
    # saved: the file is saved in some form
    # retrieval_failed: failed to retrieve the file

    # message in the retrieval. eg. error message
    message = dsaw.db.varchar(name='message', length=8192)

    # time of the retrieval


# version
__id__ = "$Id$"

# End of file 
