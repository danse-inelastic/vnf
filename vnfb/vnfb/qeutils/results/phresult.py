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
from vnfb.qeutils.results.qeresult import QEResult

NONE        = "None"

class PHResult(QEResult):

    def __init__(self, director, simid):
        self._type  = "PH"  # Important attribute
        super(PHResult, self).__init__(director, simid, self._type)


    def fildyn(self):
        "Returns formatted fildyn path"
        return "'%s'" % self._fildyn()


    def _fildyn(self):
        "Returns fildyn parameter which is the remote absolute base for matdyn files"
        # E.g.: /home/dexity/espresso/qejobs/5YWWTCQT/matdyn
        if not self.remotePath():
            return "ERROR: PH remote results directory is not available!"

        return os.path.join(self.remotePath(), FILDYN)

    
__date__ = "$Mar 22, 2010 11:40:10 PM$"

