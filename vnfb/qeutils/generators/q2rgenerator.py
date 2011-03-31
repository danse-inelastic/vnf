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

import os
from vnfb.qeutils.results.phresult import PHResult
from vnfb.qeutils.qeparser.qeinput import QEInput
from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.qeconst import ZASR, ZASRLIST

"""
Q2RGenerator - input generator class for Q2R task
"""

FLFRC   = "'default.fc'"    # formatted!

class Q2RGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None


    def setInput(self):
        "Set namelist 'input'"
        self._input     = QEInput(type='q2r')
        nl              = self._input.namelist("input")
        zasr            = ZASR[ZASRLIST[int(self._inv.zasr)]]

        nl.set("fildyn",    self.fildyn()) # from PH results
        nl.set("zasr",      zasr)
        nl.set("flfrc",     FLFRC)


    def fildyn(self):
        "Returns fildyn parameter from PH results"
        phresults       = PHResult(self._director, self._inv.id)
        return phresults.fildyn()


    def toString(self):
        return self._input.toString()

__date__ = "$Mar 24, 2010 9:59:39 AM$"


#        self._input     = QEInput(type='q2r')
#        nl              = Namelist("input")
#        self._input.addNamelist(nl)
#
#        phresults       = PHResult(self._director, self._inv.id)
#        zasr    = ZASR[ZASRLIST[int(self._inv.zasr)]]
#
#        nl.add("fildyn",    phresults.fildyn()) # from PH results
#        nl.add("zasr",      zasr)
#        nl.add("flfrc",     FLFRC_F)

