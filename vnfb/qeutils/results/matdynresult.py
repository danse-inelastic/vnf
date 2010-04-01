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
from vnfb.qeutils.qeconst import LINKORDER
from vnfb.qeutils.results.qeresult import QEResult
from qecalc.qetask.matdyntask import MatdynTask

NONE        = "None"
class MATDYNResult(QEResult):

    def __init__(self, director, simid, subtype = None):
        super(MATDYNResult, self).__init__(director, simid, linkorder = LINKORDER["MATDYN"], subtype = subtype)


    def _taskFactory(self):
        config  = "[matdyn.x]\nmatdynInput: %s\nmatdynOutput: %s" % (self._inputFile, self._outputFile)
        return MatdynTask(configString=config)


    def dosFile(self):
        "Returns path of .dos file if it exists"
        dosfile = self._resultPath.resultFiles("dos")   # phonon dos file

        if dosfile and os.path.exists(dosfile): # Check if file exists
            return dosfile

        return None

__date__ = "$Mar 22, 2010 11:40:10 PM$"


