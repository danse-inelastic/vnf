# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def createAndRunJobFullCycle(type, id, credential):
    """for the given computation (specified by type and id)
    create a job, submit it, wait for its finish, and wait for
    result retrieval to finish.
    """
    from . import run
    # create job
    jobid = run(actor='job',
        routine='createJob',
        computation_type = type,
        computation_id = id,
        credential = credential,
        )
    # tune the job props
    run(actor='job',
        routine='setAttributes',
        id = jobid,
        short_description='job for %s %s' % (type, id),
        credential = credential,
        )

    # start the job submission process
    taskid = run(actor='job',
        routine='start_submission_task',
        id = jobid,
        credential = credential,
        )
    # .. and wait for it to finish
    from .itask import waitForITaskToFinish
    waitForITaskToFinish(taskid, credential)
    
    # wait for job to finish
    from .job import waitForJobToFinish
    waitForJobToFinish(jobid, credential)
    
    # now we should have a itask running to get result
    # so we should check that itask
    taskids = run(
        actor='computation',
        routine='getTaskIds',
        type = 'material_simulations.BvKComputation.BvK_GetPhonons',
        id = id,
        iworker = 'retrieve_computation_results',
        credential = credential,
        )
    # .. as a list
    taskids = taskids.split(',')
    # .. take the only one
    assert len(taskids) == 1
    res_retrieval_taskid = taskids[0]
    # .. wait for the task of result retrieval to finish
    waitForITaskToFinish(res_retrieval_taskid, credential)
    return


# version
__id__ = "$Id$"

# End of file 
