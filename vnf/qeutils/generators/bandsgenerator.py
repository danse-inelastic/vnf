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

from vnf.qeutils.qeconst import FILBAND
from vnf.qeutils.qeparser.qeinput import QEInput

LSIM    = ".true."

class BANDSGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None


    def setInputpp(self):
        self._input     = QEInput(type="bands")
        nl      = self._input.namelist("inputpp")
        nl.add("filband",   FILBAND)
        nl.add("lsym",      LSIM)


    def toString(self):
        return self._input.toString()

__date__ = "$Mar 24, 2010 9:59:39 AM$"


