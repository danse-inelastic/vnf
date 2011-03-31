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

from vnf.qeutils.qeparser.qeinput import QEInput

class DOSGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None

    def setInputpp(self):
        self._input     = QEInput(type="dos")
        nl      = self._input.namelist("inputpp")
        nl.add("Emin",      self._inv.emin)
        nl.add("Emax",      self._inv.emax)
        nl.add("DeltaE",    self._inv.deltae)


    def toString(self):
        return self._input.toString()

__date__ = "$Mar 24, 2010 9:59:39 AM$"


