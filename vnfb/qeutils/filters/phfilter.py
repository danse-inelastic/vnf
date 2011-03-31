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
PHFilter - configuration input filter for ph task type.
"""

PREFIX  = "'pwscf'"
FILDYN  = "'matdyn'"

class PHFilter(Filter):

    def _setPlusFilter(self):
        self._plus.setParam("inputph", "prefix", PREFIX)
        self._plus.setParam("inputph", "fildyn", FILDYN)


    def _setMinusFilter(self):
        self._minus.setParam("inputph", "outdir")       # Will be set to $ESPRESSO_TMPDIR


__date__ = "$Aug 6, 2010 12:16:13 PM$"


