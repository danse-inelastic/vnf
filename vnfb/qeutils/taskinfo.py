#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

# Status: DEPRICATED for now
# XXX: Should be removed or redone to have more meaning

class TaskInfo:
    "TaskInfo - holds information about the simulation task"
    def __init__(self, simid = None, taskid = None, type = None):
        self._simid     = simid
        self._taskid    = taskid
        self._type      = type

    def simid(self):
        return self._simid

    def taskid(self):
        return self._taskid

    def type(self):
        "Type of simulation task"
        return self._type


__date__ = "$Jan 14, 2010 6:50:57 AM$"


