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


def find_pending_tasks(iworker=None, criteria=None, beneficiary=None, director=None):
    if beneficiary is None: raise ValueError
    if director is None: raise RuntimeError
    if criteria is None:
        if iworker:
            def _(item):
                label, task = item
                return task.worker == iworker
            criteria = _
        else:
            raise RuntimeError
        
    pending_tasks = beneficiary.pending_tasks.dereference(director.clerk.db)
    if not pending_tasks: return
    
    return filter(criteria, pending_tasks)


# version
__id__ = "$Id$"

# End of file 
