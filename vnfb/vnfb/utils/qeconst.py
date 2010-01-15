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

SIMULATIONS = ("Total Energy",              # 0
               "Electron DOS",              # 1
               "Electron Dispersion",       # 2 pw.x -> pw.x -> bands.x -> plotbands.x
               "Geometry Optimization",     # 3
               "Single Phonon",             # 4
               "Multiple Phonon")           # 5 DOS and Dispersion, See: example06
            
# Types of simulations
SIMCHAINS = OrderedDict()
SIMCHAINS[SIMULATIONS[0]]   = ("PW",)
SIMCHAINS[SIMULATIONS[1]]   = ("PW", "DOS")
SIMCHAINS[SIMULATIONS[2]]   = ("PW", "DOS")
SIMCHAINS[SIMULATIONS[3]]   = ("PW",)
SIMCHAINS[SIMULATIONS[4]]   = ("PW", "PH", "DYNMAT")
SIMCHAINS[SIMULATIONS[5]]   = ("PW", "PH", "Q2R", "MATDYN")


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

# Settings specific to QE
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
_zasr       = ("crystal", "simple", "one-dim", "zero-dim", "no")
ZASR        = OrderedDict()
ZASR[_zasr[0]]  = "'crystal'"
ZASR[_zasr[1]]  = "'simple'"
ZASR[_zasr[2]]  = "'one-dim'"
ZASR[_zasr[3]]  = "'zero-dim'"
ZASR[_zasr[4]]  = "'no'"

IBRAV       = ( "0.  None",                             # 0
                "1.  Cubic P (sc)",                     # 1
                "2.  Cubic F (fcc)",                    # 2
                "3.  Cubic I (bcc)",                    # 3
                "4.  Hexagonal and Trigonal P",         # 4
                "5.  Trigonal R",                       # 5
                "6.  Tetragonal P (st)",                # 6
                "7.  Tetragonal I (bct)",               # 7
                "8.  Orthorhombic P",                   # 8
                "9.  Orthorhombic base-centered(bco)",  # 9
                "10. Orthorhombic face-centered",       # 10
                "11. Orthorhombic body-centered",       # 11
                "12. Monoclinic P",                     # 12
                "13. Monoclinic base-centered",         # 13
                "14. Triclinic"                         # 14
                )

_smearing   = ("gaussian", "methfessel-paxton", "marzari-vanderbilt", "fermi-dirac")
SMEARING    = OrderedDict()
SMEARING[_smearing[0]]  = "'gauss'"
SMEARING[_smearing[1]]  = "'mp'"
SMEARING[_smearing[2]]  = "'mv'"
SMEARING[_smearing[3]]  = "'fd'"



__date__ = "$Nov 3, 2009 3:12:34 PM$"


