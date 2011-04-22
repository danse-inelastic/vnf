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


def waitForITaskToFinish(taskid, credential):
    from . import run
    import time
    while 1:
        taskstatus = run(
            actor='itask',
            routine='getStatus',
            id = taskid,
            credential = credential,
            )
        # eval to a dictionary
        taskstatus = eval(taskstatus)
        
        # check status
        if taskstatus['state'] in ['finished', 'failed', 'cancelled']:
            break
        time.sleep(5)
        continue
    
    if taskstatus['state'] != 'finished':
        raise RuntimeError, "itask %s %s" % (taskid, taskstatus['state'])
    
    return


# version
__id__ = "$Id$"

# End of file 
