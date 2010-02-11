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

from vnfb.utils.orderedDict import OrderedDict

# Available packages
PACKAGES    = ("Quantum Espresso",)  #, "VASP", "GULP"]  # Packages

# Type of configuration files
TYPE        = {"PW":    "pw.x",
               "PH":    "ph.x",
               "BANDS": "bands.x",
               "PP":    "pp.x",
               "DOS":   "dos.x",
               "Q2R":   "q2r.x",
               "MATDYN": "matdyn.x",
               "DYNMAT": "dynmat.x",
               "D3":    "d3.x"
               }
               # Other types: "CPPP", "INITIAL_STATE", "GIPAW", "D1", "MATDYN", "PROJWFC", "PWCOND"

NOPARALLEL  = ("DOS", "MATDYN", "DYNMAT", "Q2R") # "BANDS"?, "PP"? #

# Steps of job creation
STEPS       = ("Create Simulation",
               "Create Configuration",
               "Set Simulation Parameters",
               "Review Simulation")


# Types of simulations
SIMCHAINS = OrderedDict()
SIMCHAINS["Total Energy"]           = ("PW",)
SIMCHAINS["Electron DOS"]           = ("PW", "DOS")
SIMCHAINS["Electron Dispersion"]    = ("PW", "DOS") # pw.x -> pw.x -> bands.x -> plotbands.x
SIMCHAINS["Geometry Optimization"]  = ("PW",)
SIMCHAINS["Single Phonon"]          = ("PW", "PH", "DYNMAT")
SIMCHAINS["Multiple Phonon"]        = ("PW", "PH", "Q2R", "MATDYN") # DOS and Dispersion, See: example06


# Available servers
SERVERS     = ("foxtrot.danse.us",)
               #"octopod.danse.us",
               #"upgrayedd.danse.us",
               #"teragrid"

# States of a job
STATES = {
        'C': 'finished',
        'R': 'running',
        'Q': 'queued',
        'E': 'exiting', # intermediate state, Running -> Exiting -> Completed
        'H': 'onhold',  # cancelled
        'W': 'waiting',
        'S': 'suspend', # stopped
        }


PARSERS = ("qeinput",)

# Settings specific for QE and foxtrot
SETTINGS  = {
                "numproc":      8,
                "numnodes":     8,
                "npool":        8,
                "executable":   "mpirun",
                "params":       "--mca btl openib,sm,self",                       # Specific for foxtrot
                "modules":      "openmpi acml/4.3.0_gfortran64_int32 espresso"    # Specific for foxtrot
              }

# Default name of script that runs simulation of computing cluster
RUNSCRIPT   = "run.sh"

RESULTS_ID   = "results-link"

# TODO: Move to parser/inputs
ZASR        = OrderedDict()
ZASR["crystal"]     = "'crystal'"
ZASR["simple"]      = "'simple'"
ZASR["one-dim"]     = "'one-dim'"
ZASR["zero-dim"]    = "'zero-dim'"
ZASR["no"]          = "'no'"

IBRAV       = ( "Not Specified",                    # 0
                "Cubic P (sc)",                     # 1
                "Cubic F (fcc)",                    # 2
                "Cubic I (bcc)",                    # 3
                "Hexagonal and Trigonal P",         # 4
                "Trigonal R",                       # 5
                "Tetragonal P (st)",                # 6
                "Tetragonal I (bct)",               # 7
                "Orthorhombic P",                   # 8
                "Orthorhombic base-centered(bco)",  # 9
                "Orthorhombic face-centered",       # 10
                "Orthorhombic body-centered",       # 11
                "Monoclinic P",                     # 12
                "Monoclinic base-centered",         # 13
                "Triclinic"                         # 14
                )

#_smearing   = ("gaussian", "methfessel-paxton", "marzari-vanderbilt", "fermi-dirac")
SMEARING    = OrderedDict()
SMEARING["gaussian"]            = "'gauss'"
SMEARING["methfessel-paxton"]   = "'mp'"
SMEARING["marzari-vanderbilt"]  = "'mv'"
SMEARING["fermi-dirac"]         = "'fd'"

#PROCESSORS  = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36, 48, 60, 72) # ppn = 12
PROCESSORS  = (1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112)    # ppn = 8

QE_PREFIX   = "'default'"
PREFIX      = "default"

MATDYN_METHOD  = OrderedDict()
MATDYN_METHOD["dos"]           = "Phonon Density of States (DOS)"
MATDYN_METHOD["dispersion"]    = "Phonon on Grid (For Virtual Neutron Experiment)"


__date__ = "$Nov 3, 2009 3:12:34 PM$"


