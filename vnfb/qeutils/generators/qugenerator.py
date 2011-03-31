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
QUGenerator - generates Quenching configuration input based on
    Electron Minization configuration input
"""

NDW                 = "52"
RESTART_MODE        = "'reset_counters'"
ELECTRON_DYNAMICS   = "'verlet'"
ELECTRON_VELOCITIES = "'zero'"
ION_DYNAMICS        = "'verlet'"
ION_VELOCITIES      = "'zero'"

from vnf.qeutils.generators.cpgenerator import CPGenerator as base

class QUGenerator(base):
    "Generator for CP Quenching task"

    def __init__(self,  director, inventory, input = None):
        super(QUGenerator, self).__init__(director, inventory, input)

    def setControl(self):
        control  = self._input.namelist("control")
        control.set("dt", self._inv.dt)
        control.set("nstep", self._inv.nstep)
        self._setNdw(control)
        control.set("restart_mode", RESTART_MODE)   # Should restart instead?


    def setElectrons(self):
        electrons  = self._input.namelist("electrons")
        electrons.set("electron_dynamics", ELECTRON_DYNAMICS)
        electrons.add("electron_velocities", ELECTRON_VELOCITIES)


    def setIons(self):
        ions        = self._input.namelist("ions")
        ions.set("ion_dynamics", ION_DYNAMICS)
        ions.add("ion_velocities", ION_VELOCITIES)


    def _setNdw(self, control):
        "Sets 'ndw' parameter"
        if not control:
            return

        ndw         = control.param("ndw")
        if ndw:
            control.set("ndw", str(int(ndw)+1))
            return

        control.set("ndw", NDW)



__date__ = "$May 16, 2010 10:03:18 AM$"


