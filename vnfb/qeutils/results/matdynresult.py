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
from vnf.qeutils.qeconst import LINKORDER
from vnf.qeutils.results.qeresult import QEResult
from qecalc.qetask.matdyntask import MatdynTask

NONE        = "None"
class MATDYNResult(QEResult):

    def __init__(self, director, simid, subtype = None):
        super(MATDYNResult, self).__init__(director, simid, LINKORDER["MATDYN"], subtype)


    def _taskFactory(self):
        config  = "[matdyn.x]\nmatdynInput: %s\nmatdynOutput: %s" % (self._inputFile, self._outputFile)
        return MatdynTask(configString=config)


    # XXX: nk1, nk2, nk3 should be in matdyn.in!
    # XXX: Doesn't check if nk1, nk2, nk3 are digits
    def nqGrid(self):
        "Returns tuple of nq grid. No formatting"
        if not self._input:
            return None     # No input, no nq grid

        nl  = self._input.namelist("input")
        if not nl:
            return None     # No "input" namelist, no nq grid

        return (int(nl.param("nk1")), int(nl.param("nk2")), int(nl.param("nk3")))


    def pols(self):
        "Polarization. Rename and implement!"

    def freqs(self):
        "Frequencies. Rename and implement!"

__date__ = "$Mar 22, 2010 11:40:10 PM$"


