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
DYNMATFilter - configuration input filter for dynmat task type.
"""

FILOUT  = "'dynmat.out'"
FILMOL  = "'dynmat.mold'"
FILXSF  = "'dynmat.axsf'"

class DYNMATFilter(Filter):
    
    def _setPlusFilter(self):
        self._plus.setParam("input", "filout", FILOUT)
        self._plus.setParam("input", "filmol", FILMOL)
        self._plus.setParam("input", "filxsf", FILXSF)

        #{path to PH fildyn directory}, Example: '/home/danse-vnf-admin/vnf/data/qejobs/9DDA4RS/matdyn'
        #self._plus.setParam("input", "fildyn", "XXX")


__date__ = "$Aug 6, 2010 12:16:13 PM$"


