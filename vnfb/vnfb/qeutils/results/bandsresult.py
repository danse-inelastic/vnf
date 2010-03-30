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
class BANDSResult(QEResult):

    def __init__(self, director, simid):
        super(BANDSResult, self).__init__(director, simid, linkorder = LINKORDER["BANDS"])

__date__ = "$Mar 22, 2010 11:40:10 PM$"


