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

"""
IMGenerator - generates Ion Minimization configuration input based on
    Electron Minization configuration input
"""

from vnfb.qeutils.generators.cpgenerator import CPGenerator as base

class IMGenerator(base):
    "Generator for CP Ion Minimization task"

    def __init__(self,  director, inventory, input = None):
        super(IMGenerator, self).__init__(director, inventory, input)

    def setControl(self):
        control  = self._input.namelist("control")
        control.set("dt", self._inv.dt)
        control.set("nstep", self._inv.nstep)
        control.set("restart_mode", "'restart'")
        
        


__date__ = "$May 16, 2010 10:01:45 AM$"


