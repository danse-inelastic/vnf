# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from filter import Filter

TYPE    = "pw"

"""
PWFilter - configuration input filter for pw task type. 
            It combines positive and negative input filters
"""

class PWFilter(Filter):

    def _setPlusFilter(self):
        self._plus.setParam("control", "prefix", "'pwscf'")


    def _setMinusFilter(self):
        self._minus.setParam("control", "pseudo_dir")   # Set by $ESPRESSO_PSEUDO
        self._minus.setParam("control", "outdir")       # Set by $ESPRESSO_TMPDIR


__date__ = "$Aug 6, 2010 12:16:13 PM$"


