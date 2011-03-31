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

NDW                 = "52"
ELECTRON_DYNAMICS   = "'damp'"
ELECTRON_DAMPING    = "0.2"
ION_DYNAMICS        = "'damp'"
ION_DAMPING         = "0.02"

from vnf.qeutils.generators.cpgenerator import CPGenerator as base

class IMGenerator(base):
    "Generator for CP Ion Minimization task"

    def __init__(self,  director, inventory, input = None):
        super(IMGenerator, self).__init__(director, inventory, input)

    def setControl(self):
        control  = self._input.namelist("control")
        control.set("dt", self._inv.dt)
        control.set("nstep", self._inv.nstep)
        self._setNdw(control)
        #control.set("restart_mode", "'restart'")   # Should restart instead?


    def setElectrons(self):
        electrons  = self._input.namelist("electrons")
        electrons.set("electron_dynamics", ELECTRON_DYNAMICS)
        electrons.set("electron_damping", ELECTRON_DAMPING)


    def setIons(self):
        ions        = self._input.namelist("ions")
        ions.set("ion_dynamics", ION_DYNAMICS)
        ions.set("ion_damping", ION_DAMPING)


    def _setNdw(self, control):
        "Sets 'ndw' parameter"
        if not control:
            return

        ndw         = control.param("ndw")
        if ndw:
            control.set("ndw", str(int(ndw)+1))
            return

        control.set("ndw", NDW)


__date__ = "$May 16, 2010 10:01:45 AM$"


