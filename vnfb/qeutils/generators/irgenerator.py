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
IRGenerator - generates Ion Randomization configuration input based on
    Electron Minization configuration input
"""

NDW                 = "52"
ELECTRON_DYNAMICS   = "'damp'"
ELECTRON_DAMPING    = "0.2"
ION_DYNAMICS        = "'none'"
TRANP               = ".true."
#AMPRP               = "0.02"


from vnfb.qeutils.generators.cpgenerator import CPGenerator as base

class IRGenerator(base):
    "Generator for CP Ion Randomization task"

    def __init__(self,  director, inventory, input = None):
        super(IRGenerator, self).__init__(director, inventory, input)

    def setControl(self):
        control  = self._input.namelist("control")
        control.set("dt", self._inv.dt)
        control.set("nstep", self._inv.nstep)
        self._setNdw(control)
        control.set("restart_mode", "'restart'") 


    def setElectrons(self):
        electrons  = self._input.namelist("electrons")
        electrons.set("electron_dynamics", ELECTRON_DYNAMICS)
        electrons.set("electron_damping", ELECTRON_DAMPING)


    def setIons(self):
        ions        = self._input.namelist("ions")
        ions.set("ion_dynamics", ION_DYNAMICS)
        ions.add("tranp(1)", TRANP)
        ions.add("amprp(1)", self._inv.amprp)


    def _setNdw(self, control):
        "Sets 'ndw' parameter"
        if not control:
            return

        ndw         = control.param("ndw")
        if ndw:
            control.set("ndw", str(int(ndw)+1))
            return

        control.set("ndw", NDW)


__date__ = "$May 16, 2010 10:02:07 AM$"


