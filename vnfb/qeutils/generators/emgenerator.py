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

from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.qeparser.card import Card
from vnfb.qeutils.qeconst import SMEARING, MATTER_TYPE, SIMTYPE, RELAXLIST
from vnfb.qeutils.results.pwresult import PWResult

# Default Control params
CALCULATION     = "'cp'"
RESTART_MODE    = "'from_scratch'"
TSTRESS         = ".true."
TPRNFOR         = ".true."
NDR             = "51"
NDW             = "51"
IPRINT          = "10"
ISAVE           = "100"
ETOT_CONV_THR   = "1.d-4"
EKIN_CONV_THR   = "1.d-6"


# Default System params
CELLDM          = "10.2"

# Default Electron params
CONV_THR        = "1.0d-8"
MIXING_BETA     = "0.7"

# Geometry: ions
ION_DYNAMICS        = "'bfgs'"
POT_EXTRAPOLATION   = "'atomic'"
WFC_EXTRAPOLATION   = "'none'"
UPSCALE             = "10.0"
BFGS_NDIM           = "1"
TRUST_RADIUS_MAX    = "0.8"
TRUST_RADIUS_MIN    = "0.001"
CELL_DYNAMICS       = "'bfgs'"



# XXX: Critical: celldm(1) is created incorrectly from atomic structure
#   Quick fix: set fixed value!
class EMGenerator(object):
    "Generator for CP Electronic Minimization task"
    
    def __init__(self, director, inventory, input = None):
        self._director  = director
        self._inv       = inventory
        self._input     = input


    def setControl(self):
        "CONTROL namelist"
        control = Namelist("control")
        self._input.addNamelist(control)
        control.add("calculation",  CALCULATION)
        control.add("restart_mode", RESTART_MODE)
        control.add("ndr",          NDR)
        control.add("ndw",          NDW)
        control.add("nstep",        self._inv.nstep)
        control.add("iprint",       IPRINT)
        control.add("isave",        ISAVE)
        control.add("tstress",      TSTRESS)
        control.add("tprnfor",      TPRNFOR)
        control.add("dt",           self._inv.dt)
        control.add("etot_conv_thr", ETOT_CONV_THR)
        control.add("ekin_conv_thr", EKIN_CONV_THR)


    def setSystem(self):
        "SYSTEM namelist"
        system  = self._input.namelist("system")  # System namelist already exists
        system.add("ecutwfc", self._inv.ecutwfc)
        system.set("celldm(1)", CELLDM) # XXX: Hack


#    def setElectrons(self):         # TODO: Suitable for phonon calculations?
#        "ELECTRONS namelist"
#        electrons   = Namelist("electrons")
#        electrons.add("conv_thr",       CONV_THR)
#        electrons.add("mixing_beta",    MIXING_BETA)
#        self._input.addNamelist(electrons)
#
#
#    def setIons(self):
#        ions        = Namelist("ions")
#        self._input.addNamelist(ions)
#        ions.add("ion_dynamics",        ION_DYNAMICS)
#        ions.add("pot_extrapolation",   POT_EXTRAPOLATION)
#        ions.add("wfc_extrapolation",   WFC_EXTRAPOLATION)
#        ions.add("upscale",             UPSCALE)
#        ions.add("bfgs_ndim",           BFGS_NDIM )
#        ions.add("trust_radius_max",    TRUST_RADIUS_MAX)
#        ions.add("trust_radius_min",    TRUST_RADIUS_MIN)
#
#
#    def setCell(self):
#        cell    = Namelist("cell")
#        self._input.addNamelist(cell)
#

    def toString(self):
        return self._input.toString()#structure.toString()


    
__date__ = "$May 16, 2010 10:01:22 AM$"


