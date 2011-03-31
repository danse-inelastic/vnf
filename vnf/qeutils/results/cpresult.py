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

import os
from qecalc.qetask.cptask import CPTask
from vnf.qeutils.results.qeresult import QEResult

NONE        = "None"
class CPResult(QEResult):

    def __init__(self, director, simid, linkorder, tasktype = None):
        super(CPResult, self).__init__(director, simid, linkorder = linkorder)
        self._tasktype  = tasktype


    def _taskFactory(self):
        "Factory for cp task"
        # Uncomment when the CPTask is fixed
        config  = "[cp.x]\ncpInput: %s\ncpOutput: %s" % (self._inputFile, self._outputFile)
        return CPTask(configString=config)


__date__ = "$May 17, 2010 11:47:17 AM$"


