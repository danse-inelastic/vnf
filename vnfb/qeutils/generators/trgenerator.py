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

import StringIO
import ConfigParser

VELFILE     = "cp.vel"
POSFILE     = "cp.pos"
NCFILE      = "cp.nc"
DOSFILE     = "vdos.dos"

class TRGenerator(object):
    "Generator for CP Trajectory Analysis task"

    def __init__(self, director, inventory, input = None):
        self._director  = director
        self._inv       = inventory
        self._input     = input

        self._init()


    def _init(self):
        if not self._input:
            self._fp    = StringIO.StringIO()
            self._input = ConfigParser.ConfigParser()


    def setSystem(self):
        "Sets system parameters"
        self._input.add_section("system")
        self._input.set("system", "fvel",   VELFILE)    # Velocities file
        self._input.set("system", "fpos",   POSFILE)    # Position file
        self._input.set("system", "fnc",    NCFILE)     # Trajectory file in netCDF format
        self._input.set("system", "fdos",   DOSFILE)    # Dos file


    def setSteps(self):
        "Sets system parameters"
        self._input.add_section("steps")
        self._input.set("steps", "start", self._inv.start)
        self._input.set("steps", "end", self._inv.end)


    def setAnalysis(self):
        "Sets analysis specific parameters"
        self._input.add_section("analysis")
        self._input.set("analysis", "vdos", self._inv.vdos)     # Vibrational Density of States (VDOS)
        self._input.set("analysis", "vdist", self._inv.vdist)   # Velocity Distribution
        self._input.set("analysis", "msd", self._inv.msd)       # Mean-Square Displacement
        self._input.set("analysis", "rdf", self._inv.rdf)       # Radial Distribution Function
        self._input.set("analysis", "temptime", self._inv.temptime) # Temperature Dependence on Time


    def toString(self):
        if not self._input:
            return "TRGenerator"

        self._input.write(self._fp)
        str = self._fp.getvalue()
        self._fp.close()
        return str

        

__date__ = "$May 16, 2010 10:04:49 AM$"


