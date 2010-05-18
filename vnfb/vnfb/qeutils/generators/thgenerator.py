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

from vnfb.qeutils.generators.cpgenerator import CPGenerator as base

# Control namelist
#RESTART_MODE    = "'restart'"
RESTART_MODE    = "'reset_counters'"
NDW             = "52"

# Electrons namelist
ELECTRON_DYNAMICS   = "'verlet'"

# Ions namelist
ION_DYNAMICS    = "'verlet'"
ION_TEMPERATURE = "'nose'"


# XXX: Revise defaults!

class THGenerator(base):
    "Generator for CP Dynamics with Thermostat task"

    def setControl(self):
        "CONTROL namelist"
        control = self._input.namelist("control")
        control.set("restart_mode", RESTART_MODE)
        control.set("ndw",          NDW)
        control.set("dt",           self._inv.dt)
        control.set("nstep",        self._inv.nstep)


    def setElectrons(self):
        "ELECTRONS namelist"
        electrons   = self._input.namelist("electrons")
        electrons.set("electron_dynamics",  ELECTRON_DYNAMICS)
        electrons.remove("electron_temperature")


    def setIons(self):
        "IONS namelist"
        ions        = self._input.namelist("ions")
        ions.set("ion_dynamics",    ION_DYNAMICS)
        ions.add("ion_temperature", ION_TEMPERATURE)
        ions.add("tempw",           self._inv.tempw)
        ions.add("fnosep",          self._inv.fnosep)


__date__ = "$May 16, 2010 10:04:32 AM$"


