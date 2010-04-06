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

from vnfb.qeutils.qeconst import LINKORDER
from vnfb.qeutils.results.qeresult import QEResult

NONE        = "None"
class PLOTBANDResult(QEResult):

    def __init__(self, director, simid):
        super(PLOTBANDResult, self).__init__(director, simid, linkorder = LINKORDER["PLOTBAND"])


    def bandsPS(self):
        "Returns plotbands ps file"
        return self._resultPath.resultFiles("psband", relative = True)

__date__ = "$Mar 22, 2010 11:40:10 PM$"


