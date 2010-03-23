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

from vnfb.qeutils.results.qeresult import QEResult

NONE        = "None"
class Q2RResult(QEResult):

    def __init__(self, director, simid):
        self._type  = "Q2R"  # Important attribute
        super(Q2RResult, self).__init__(director, simid, self._type)


__date__ = "$Mar 22, 2010 11:40:10 PM$"


