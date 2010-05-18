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

from vnfb.qeutils.results.cpresult import CPResult
from vnfb.qeutils.qeparser.qeinput import QEInput

EM_LINKORDER    = 0 # Electron minimization should exist!

class IMGenerator(object):
    "Generator for CP Ion Minimization task"

    def __init__(self, director, inventory, input = None):
        self._director  = director
        self._inv       = inventory
        self._input     = input

        self._init(director)


    def _init(self, director):
        if not self._input:
            self._input = self._cpInput(director)


    def _cpInput(self, director):
        "Take input file from results and create QEInput object"
        result      = CPResult(director, self.id, linkorder = EM_LINKORDER)
        inputFile   = result.inputFile()
        input = QEInput(filename = inputFile, type = "cp")
        input.parse()
        return input


    def toString(self):
        if not self._input:
            return "IMGenerator"

        return self._input.toString()
        

__date__ = "$May 16, 2010 10:01:45 AM$"


