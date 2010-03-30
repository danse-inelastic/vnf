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
from qecalc.qetask.q2rtask import Q2RTask
from vnfb.qeutils.qeconst import LINKORDER
from vnfb.qeutils.results.qeresult import QEResult

NONE    = "None"
FLFRC   = "default.fc"

class Q2RResult(QEResult):

    def __init__(self, director, simid):
        super(Q2RResult, self).__init__(director, simid, linkorder = LINKORDER["Q2R"])


    def zasr(self):
        if not self._input: # No input file
            return "ERROR: Q2R input file is not available!"
        
        zasr    = self._input.namelist("input").param("zasr")
        if not zasr:        # No zasr parameter
            return "ERROR: Parameter 'zasr' is not in the Q2R input file!"

        return zasr
        

    def flfrc(self):
        return "'%s'" % self._flfrc()


    def _flfrc(self):
        "Returns force constants path (default.fc) from remote results directory"
        if not self.remotePath():
            return "ERROR: Q2R remote results directory is not available!"

        return os.path.join(self.remotePath(), FLFRC)


    def _taskFactory(self):
        "Factory for q2r task"
        config  = "[q2r.x]\nq2rInput: %s\nq2rOutput: %s" % (self._inputFile, self._outputFile)
        return Q2RTask(configString=config)


__date__ = "$Mar 22, 2010 11:40:10 PM$"


