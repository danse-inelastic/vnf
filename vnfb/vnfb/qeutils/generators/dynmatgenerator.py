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

from vnfb.qeutils.qeparser.qeinput import QEInput
from vnfb.qeutils.qeparser.namelist import Namelist

class DYNMATGenerator(object):

    def __init__(self, inventory, input):
        self._inv       = inventory
        self._input     = input


    def setInput(self):
        self._input      = QEInput(type='dynmat')
        nl  = Namelist("input")
        self._input.addNamelist(nl)


    def toString(self):
        return self._input.toString()


__date__ = "$Mar 24, 2010 9:59:39 AM$"


