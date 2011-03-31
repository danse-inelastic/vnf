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

"""
PWFilter - configuration input filter for pw task type. 
"""

PREFIX  = "'pwscf'"

class PWFilter(Filter):

    def _setPlusFilter(self):
        self._plus.setParam("control", "prefix", PREFIX)


    def _setMinusFilter(self):
        self._minus.setParam("control", "pseudo_dir")   # Will be set to $ESPRESSO_PSEUDO
        self._minus.setParam("control", "outdir")       # Will be set to $ESPRESSO_TMPDIR


__date__ = "$Aug 6, 2010 12:16:13 PM$"


