# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def retrieve_results(computation, director):
    'retrieve results of computation'
    
    # get handler
    name = computation.getResultRetrieverName()
    retriever = director.retrieveComponent(
        name, factory='retriever', vault=['result_retrievers'])
    if retriever is None:
        curator_dump = director._dumpCurator()
        raise RuntimeError, "could not load result retriever %r. curator dump: %s" % (
            name, curator_dump)
    retriever.director = director

    # run retriever
    return retriever.run(computation)


iworker_results_retrieval = 'retrieve_computation_results'
def start_results_retrieval(computation, director):
    iworker = iworker_results_retrieval
    # create an itask
    task = get_results_retrieval_task(computation, director.clerk.db)
    if not task:
        from vnf.dom.ITask import createITask, ITask
        task = director.clerk.insertNewOwnedRecord(ITask)
        task = createITask(
            task.id,
            beneficiary = computation,
            worker = iworker,
            type = iworker,
            )
        director.clerk.updateRecordWithID(task)
    else:
        if task.state not in ['failed', 'cancelled']:
            # should not reach here
            raise RuntimeError, \
                  "failed to understand itask %s(%s) for computation %s." % (
                iworker, task.id, computation.id)
        # reopen the task
        task.state = 'created'
        director.clerk.updateRecordWithID(task)

    # start the task
    from vnf.utils.itask import start
    start(task)
    #
    return


def get_results_retrieval_task(computation, db):
    # create an itask
    iworker = iworker_results_retrieval
    task = computation.findPendingTask(db, iworker=iworker)
    return task

# version
__id__ = "$Id$"

# End of file 
