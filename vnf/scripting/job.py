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


def waitForJobToFinish(jobid, credential):
    from . import run
    import time
    while 1:
        jobstatus = run(
            actor = 'job',
            routine = 'updateStatus',
            id = jobid,
            credential = credential,
            )
        if jobstatus in ['submitted', 'running', 'queued']:
            print 'job #%s is %s' % (jobid, jobstatus)
        elif jobstatus in ['finished', 'terminated', 'cancelled']:
            break
        else:
            raise RuntimeError, "job %s status is %s" % (jobid, jobstatus)
        time.sleep(5)
        continue
    
    if jobstatus != 'finished':
        raise RuntimeError, "job %s is %s" % (jobid, jobstatus)

    return


# version
__id__ = "$Id$"

# End of file 
