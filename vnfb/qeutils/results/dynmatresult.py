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

from qecalc.qetask.dynmattask import DynmatTask
from vnf.qeutils.qeconst import LINKORDER
from vnf.qeutils.results.qeresult import QEResult

NONE        = "None"
class DYNMATResult(QEResult):

    def __init__(self, director, simid):
        super(DYNMATResult, self).__init__(director, simid, linkorder = LINKORDER["DYNMAT"])


    def _taskFactory(self):
        config  = """[dynmat.x]
dynmatInput: %s
dynmatOutput: %s
filout: %s""" % (self._inputFile,
                 self._outputFile,
                 self._resultPath.resultFiles("filout"))
        return DynmatTask(configString=config)


__date__ = "$Mar 22, 2010 11:40:10 PM$"


