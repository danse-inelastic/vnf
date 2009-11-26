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
TYPES       = ("PW", "PH", "PP")  # "BANDS", "CPPP", "D3", "DOS", "DYNMAT", "INITIAL_STATE", "GIPAW", "D1", "MATDYN", "PROJWFC", "PWCOND", "Q2R" 

# Steps of job creation
STEPS       = ("Create Simulation",
               "Create Configuration",
               "Set Simulation Parameters",
               "Review Simulation")

SIMULATIONS = ("Total Energy",              # 0
               "Electron DOS",              # 1
               "Electron Dispersion",       # 2
               "Geometry Optimization",     # 3
               "Single-Phonon",             # 4
               "Multi-Phonon DOS",          # 5
               "Multi-Phonon Dispersion")   # 6
            
# Types of simulations
SIMCHAINS = OrderedDict()
SIMCHAINS[SIMULATIONS[0]]   = ("PW",)
SIMCHAINS[SIMULATIONS[1]]   = ("PW", "DOS")
SIMCHAINS[SIMULATIONS[2]]   = ("PW", "DOS")
SIMCHAINS[SIMULATIONS[3]]   = ("PW",)
SIMCHAINS[SIMULATIONS[4]]   = ("PW", "PH", "DYNMAT")
SIMCHAINS[SIMULATIONS[5]]   = ("PW", "PH", "Q2R", "MATDYN")
SIMCHAINS[SIMULATIONS[6]]   = ("PW", "PH", "Q2R", "MATDYN")


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
QESETTINGS  = {
                "server":       "Server Name",
                "numproc":      "Number of Processors",
                "numnodes":     "Number of Nodes",
                "procpernode":  "Processors Per Node",
                "npool":        "Npool",
                "executable":   "Executable",
                "params":       "Additional Parameters",
                "qemodules":    "Modules"
              }


__date__ = "$Nov 3, 2009 3:12:34 PM$"


