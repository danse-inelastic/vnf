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
from vnfb.qeutils.results.qeresult import QEResult

NONE        = "None"
class CPResult(QEResult):

    def __init__(self, director, simid, tasktype, linkorder):
        super(CPResult, self).__init__(director, simid, linkorder = linkorder)

__date__ = "$May 17, 2010 11:47:17 AM$"


