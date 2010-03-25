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
from vnfb.qeutils.qeparser.qeinput import QEInput
from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.qeconst import ZASR, ZASRLIST, PREFIX, FILDYN
from vnfb.qeutils.results.resultpath import ResultPath

"""
Q2RGenerator - input generator class for Q2R task
"""

class Q2RGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None


    def setInput(self):
        "Set namelist 'input'"
        self._input     = QEInput(type='q2r')
        nl              = Namelist("input")
        self._input.addNamelist(nl)

        # Get jobs directory of PH simulation task
        resultpath  = ResultPath(self._director, self._inv.id, "PH")
        path        = resultpath.resultPath()
        # E.g.: /home/dexity/espresso/qejobs/5YWWTCQT/matdyn
        fildyn  = os.path.join(path, FILDYN)  # "matdyn" - default value for PH fildyn
        zasr    = ZASR[ZASRLIST[int(self._inv.zasr)]]

        nl.add("fildyn",    "'%s'" % fildyn)
        nl.add("zasr",      zasr)
        nl.add("flfrc",     "'%s.fc'" % PREFIX)  # XXX
        

    def toString(self):
        return self._input.toString()

__date__ = "$Mar 24, 2010 9:59:39 AM$"


