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
from vnf.qeutils.results.resultpath import FILBAND

NONE        = "None"
class BANDSResult(QEResult):

    def __init__(self, director, simid):
        super(BANDSResult, self).__init__(director, simid, linkorder = LINKORDER["BANDS"])


    def bandsFile(self):
        "bands.dat on remote cluster"
        path    = self._resultPath.remotePath()
        return os.path.join(path, FILBAND)

__date__ = "$Mar 22, 2010 11:40:10 PM$"


