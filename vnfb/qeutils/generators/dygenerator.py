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
DYGenerator - generates Electron and Ion Dynamics configuration input based on
    Electron Minization configuration input
"""

RESTART_MODE        = "'restart'"
NDW                 = "52"
NDR                 = "52"
ELECTRON_DYNAMICS   = "'verlet'"
ELECTRON_TEMPERATURE    = "'not_controlled'"
ION_DYNAMICS        = "'verlet'"

from vnf.qeutils.generators.cpgenerator import CPGenerator as base

class DYGenerator(base):
    "Generator for CP Electron and Ion Dynamics task"

    def __init__(self,  director, inventory, input = None):
        super(DYGenerator, self).__init__(director, inventory, input)


    def setControl(self):
        control  = self._input.namelist("control")
        control.set("restart_mode", RESTART_MODE)
        control.set("dt", self._inv.dt)
        control.set("nstep", self._inv.nstep)
        self._setNd(control, "ndw")
        self._setNd(control, "ndr")


    def setElectrons(self):
        electrons  = self._input.namelist("electrons")
        electrons.set("electron_dynamics", ELECTRON_DYNAMICS)
        electrons.add("electron_temperature", ELECTRON_TEMPERATURE)


    def setIons(self):
        ions        = self._input.namelist("ions")
        ions.set("ion_dynamics", ION_DYNAMICS)


    def _setNd(self, control, name):
        "Sets 'ndw' and 'ndr' parameter"
        if not control:
            return

        nd         = control.param(name)
        if nd:
            control.set(name, str(int(nd)+1))
            return

        control.set(name, NDW)


__date__ = "$May 16, 2010 10:02:45 AM$"


