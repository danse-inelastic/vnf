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


    def bandsPS(self, relative = False):
        "Returns plotbands ps file"
        return self._resultPath.resultFiles("psband", relative)


    def bandsPNG(self):
        "Returns bands.png file converted from bands.ps"
        pngfile     = self._resultPath.resultFiles("pngband")
        if pngfile:    # If file exists, just return it
            return pngfile

        # Otherwise try to convert: ps -> png
        psfile     = self._resultPath.resultFiles("psband")
        return self._ps2png(psfile)


    def _ps2png(self, filename):
        "Converts bands.ps -> bands.png and returns absolute filename"
        return None

__date__ = "$Mar 22, 2010 11:40:10 PM$"


