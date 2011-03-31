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
PLOTBANDFilter - configuration input filter for plotband task type.
"""

class PLOTBANDFilter(Filter):
    pass

#    def _setMinusFilter(self):
#        self._minus.setParam("control", "prefix")        # Will be set to default ('pwscf')
#        self._minus.setParam("control", "pseudo_dir")   # Will be set to $ESPRESSO_PSEUDO
#        self._minus.setParam("control", "outdir")       # Will be set to $ESPRESSO_TMPDIR


__date__ = "$Aug 6, 2010 12:16:13 PM$"


