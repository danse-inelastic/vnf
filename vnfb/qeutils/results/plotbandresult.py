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
from vnfb.qeutils.results.resultpath import PNGBAND

NONE        = "None"
class PLOTBANDResult(QEResult):

    def __init__(self, director, simid):
        super(PLOTBANDResult, self).__init__(director, simid, linkorder = LINKORDER["PLOTBAND"])


    def bandsPS(self, relative = False):
        "Returns plotbands ps file"
        return self._resultPath.resultFiles("psband", relative)


    def bandsPNG(self, relative = False):
        "Returns bands.png file converted from bands.ps"
        pngfile     = self._resultPath.resultFiles("pngband")   # Absolute
        if pngfile:    # If file exists, just return it
            fpngfile     = self._resultPath.resultFiles("pngband", relative)
            return fpngfile

        # Otherwise try to convert: ps -> png
        psfile      = self._resultPath.resultFiles("psband")
        return self._ps2png(psfile, relative)


    def _ps2png(self, filename, relative):
        "Try to converts bands.ps -> bands.png and returns absolute filename"
        try:
            pspath  = self.bandsPS()
            pngpath = os.path.join(self._resultPath.localPath(), PNGBAND)   # Absolute

            # Rotate 90 degrees and convert .ps -> .png
            from PythonMagick import Image
            img     = Image(pspath)
            img.rotate(90)          # For some reason plotband.x rotates image
            img.write(pngpath)      # Write to .png file

            fpngpath = os.path.join(self._resultPath.localPath(relative), PNGBAND) # Format dependent
            return fpngpath         # If success, return path to .png file
        except:
            return None


__date__ = "$Mar 22, 2010 11:40:10 PM$"


