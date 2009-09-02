#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class ITaskProgress:

    def __init__(self, taskid, label='', id=None, sentry=None, finished_callback=''):
        if not id:
            id = __builtins__['id'](self)
        self.id = id
        
        self.label = label
        self.taskid = taskid
        self.sentry = sentry
        self.finished_callback = finished_callback
        return

    def identify(self, visitor):
        return visitor.onITaskProgress(self)


# version
__id__ = "$Id$"

# End of file 
