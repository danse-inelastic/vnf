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
MATDYNFilter - configuration input filter for matdyn task type.
"""

FLDOS   = "'matdyn.dos'"
FLFRQ   = "'matdyn.freq'"
FLVEC   = "'matdyn.modes'"

class MATDYNFilter(Filter):
    
    def _setPlusFilter(self):
        self._plus.setParam("input", "fldos", FLDOS)
        self._plus.setParam("input", "flfrq", FLFRQ)
        self._plus.setParam("input", "flvec", FLVEC)


    def setFlfrc(self, flfrc):
        "Dynamically sets filter for flfrc"
        # Path do Q2R flfrc directory. Example: '/home/danse-vnf-admin/vnf/data/qejobs/9S2EA6Z/default.fc'
        self._plus.setParam("input", "flfrc", flfrc)


__date__ = "$Aug 6, 2010 12:16:13 PM$"


