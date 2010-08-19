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
Q2RFilter - configuration input filter for q2r task type.
"""

FLFRC   = "'default.fc'"

class Q2RFilter(Filter):

    def setFildyn(self, fildyn):
        "Dynamically sets filter for fildyn"
        # Path to PH fildyn directory. Example: '/home/danse-vnf-admin/vnf/data/qejobs/9DDA4RS/matdyn'
        self._plus.setParam("input", "fildyn", fildyn)


    def _setPlusFilter(self):
        self._plus.setParam("input", "flfrc", FLFRC)
        


__date__ = "$Aug 6, 2010 12:16:13 PM$"


