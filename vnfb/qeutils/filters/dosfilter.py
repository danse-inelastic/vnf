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
DOSFilter - configuration input filter for dos task type.
"""

PREFIX  = "'pwscf'"
FILDOS  = "pwscf.dos"   # Set apostrophes?

class DOSFilter(Filter):
    
    def _setPlusFilter(self):
        self._plus.setParam("inputpp", "prefix", PREFIX)
        self._plus.setParam("inputpp", "filband", FILDOS)


    def _setMinusFilter(self):
        self._minus.setParam("inputpp", "outdir")       # Will be set to $ESPRESSO_TMPDIR


__date__ = "$Aug 6, 2010 12:16:13 PM$"


