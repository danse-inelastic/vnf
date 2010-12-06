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

from vnfb.qeutils.results.phresult import PHResult
from vnfb.qeutils.qeparser.qeinput import QEInput
from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.qeconst import ZASR, ZASRLIST

class DYNMATGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None
        self._phresults = PHResult(self._director, self._inv.id)


    def setInput(self):
        "Set namelist 'input'"
        self._input      = QEInput(type='dynmat')
        nl  = Namelist("input")
        self._input.addNamelist(nl)

        nl.add("fildyn",    self._phresults.fildyn()) # from PH results
        self._addAsr(nl)
        self._addQPoint(nl)


    def fildyn(self):
        "Returns fildyn parameter from PH results"
        return self._phresults.fildyn()


    def _addAsr(self, nl):
        "Adds 'asr' parameter for gamma point only"
        if self._phresults.isGammaPoint():
            asr         = ZASR[ZASRLIST[int(self._inv.asr)]]
            nl.add("asr",      asr)


    def _addQPoint(self, nl):
        "Adds q point"
        kp          = self._phresults.kCoord()
        if not kp or type(kp) != list:
            nl.add("q(#)", "ERROR: Phonon coordinate (Kx, Ky, Kz) are not set on PH input")

        for i in range(len(kp)):
            nl.add("q(%s)" % str(i+1), kp[i])


    def toString(self):
        return self._input.toString()


__date__ = "$Mar 24, 2010 9:59:39 AM$"


