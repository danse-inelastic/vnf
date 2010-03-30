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
from vnfb.qeutils.qeconst import FILDYN
from vnfb.qeutils.qeconst import LINKORDER
from vnfb.qeutils.results.qeresult import QEResult
from qecalc.qetask.phtask import PHTask

NONE        = "None"

class PHResult(QEResult):

    def __init__(self, director, simid):
        super(PHResult, self).__init__(director, simid, linkorder = LINKORDER["PH"])


    def _taskFactory(self):
        config  = "[ph.x]\nphInput: %s\nphOutput: %s" % (self._inputFile, self._outputFile)
        return PHTask(configString=config)


    def fildyn(self):
        "Returns formatted fildyn path"
        return "'%s'" % self._fildyn()


    def isGammaPoint(self):
        "Checks if point is gamma point"
        kp  = self.kCoord()
        if not kp:
            return False

        return kp[0] == 0.0 and kp[1] == 0.0 and kp[2] == 0.0


    def kCoord(self):
        "Returns K coordinate of phonon in single phonon simulation type"
        line    = self.firstAttachLine()
        if not line:        # If no line
            return None

        kp      = line.split()
        if len(kp) != 3:  # Should have 3 elements
            return None

        return (float(kp[0]), float(kp[1]), float(kp[2]))


    def _fildyn(self):
        "Returns fildyn parameter which is the remote absolute base for matdyn files"
        # E.g.: /home/dexity/espresso/qejobs/5YWWTCQT/matdyn
        if not self.remotePath():
            return "ERROR: PH remote results directory is not available!"

        return os.path.join(self.remotePath(), FILDYN)


    def firstAttachLine(self):
        "Returns the first line of the attach"
        if not self._input: # No input, no gamma point
            return None
        
        attach  = self._input.attach        # XXX: Replace by method attach()
        if not attach:      # No attach, no gamma point
            return None
        
        lines   = attach.splitlines()
        if len(lines) > 0:  # At least one list should exist
            return lines[0] # Phonon coordinates are supposed to be on the first line

        return None
    
__date__ = "$Mar 22, 2010 11:40:10 PM$"

