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
TYPE        = {"PW":        "pw.x",
               "PH":        "ph.x",
               "BANDS":     "bands.x",
               "PLOTBAND":  "plotband.x",
               "PP":        "pp.x",
               "DOS":       "dos.x",
               "Q2R":       "q2r.x",
               "MATDYN":    "matdyn.x",
               "DYNMAT":    "dynmat.x",
               "D3":        "d3.x"
               }
               # Other types: "CPPP", "INITIAL_STATE", "GIPAW", "D1", "MATDYN", "PROJWFC", "PWCOND"

INPUT_EXT   = ".in"
OUTPUT_EXT  = ".out"

INPUT           = OrderedDict()
INPUT["pw"]     = "pw" + INPUT_EXT
INPUT["ph"]     = "ph" + INPUT_EXT
INPUT["bands"]  = "bands" + INPUT_EXT
INPUT["pp"]     = "pp" + INPUT_EXT
INPUT["dos"]    = "dos" + INPUT_EXT
INPUT["q2r"]    = "q2r" + INPUT_EXT
INPUT["matdyn"] = "matdyn" + INPUT_EXT
INPUT["dynmat"] = "dynmat" + INPUT_EXT
INPUT["d3"]     = "d3" + INPUT_EXT


NOPARALLEL  = ("DOS", "MATDYN", "DYNMAT", "Q2R", "BANDS", "PLOTBAND") # "BANDS"?, "PP"? # "PLOTBAND"?

# Obsolete: Steps of job creation
STEPS       = ("Create Simulation",
               "Create Configuration",
               "Set Simulation Parameters",
               "Review Simulation")

SIMTYPE     = OrderedDict()
SIMTYPE["scf"]                  = "Electron Structure"
SIMTYPE["electron-dos"]         = "Electron DOS"
SIMTYPE["electron-dispersion"]  = "Electron Dispersion"
SIMTYPE["geometry"]             = "Geometry Optimization"
SIMTYPE["single-phonon"]        = "Single Phonon"
SIMTYPE["multiple-phonon"]      = "Multiple Phonon"

# Types of simulations
SIMCHAINS   = OrderedDict()
SIMCHAINS[SIMTYPE["scf"]]                   = ("PW",)
SIMCHAINS[SIMTYPE["electron-dos"]]          = ("PW", "PW", "DOS")
SIMCHAINS[SIMTYPE["electron-dispersion"]]   = ("PW", "PW", "BANDS", "PLOTBAND") # pw.x -> pw.x -> bands.x -> plotbands.x
SIMCHAINS[SIMTYPE["geometry"]]              = ("PW",)
SIMCHAINS[SIMTYPE["single-phonon"]]         = ("PW", "PH", "DYNMAT")
SIMCHAINS[SIMTYPE["multiple-phonon"]]       = ("PW", "PH", "Q2R", "MATDYN") # DOS and Dispersion, See: example06
#SIMCHAINS["Molecular Dynamics"]     = ()   - Next step

SIMLIST     = SIMTYPE.values()  #SIMCHAINS.keys()

# Analysis actors
ANALYSIS    = OrderedDict()
ANALYSIS[SIMLIST[0]]    = "electron"
ANALYSIS[SIMLIST[1]]    = "electron-dos"
ANALYSIS[SIMLIST[2]]    = "electron-dispersion"
ANALYSIS[SIMLIST[3]]    = "geometry"
ANALYSIS[SIMLIST[4]]    = "phonon-single"
ANALYSIS[SIMLIST[5]]    = "phonon-multiple"

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


#    submitting  (None)
#    submit-failed   (None)
#    finished    ('C')
#    running     ('R')
#    queued      ('Q')
#    exiting     ('E')
#    onhold      ('H')
#    waiting     ('W')
#    suspend     ('S')



#(percentage, description)
JOB_STATE   = OrderedDict()
JOB_STATE["create-job"]         = (10, "Creating job record ...")
JOB_STATE["prepare-configs"]    = (20, "Preparing configuration files ...")
JOB_STATE["prepare-controls"]   = (40, "Preparing control files ...")
JOB_STATE["copy"]               = (60, "Copying files to cluster ...")
JOB_STATE["enqueue"]            = (80, "Submitting to queue ...")
JOB_STATE["submitted"]          = (100, "Done")


PARSERS = ("qeinput",)

# Settings specific for QE and foxtrot
SETTINGS  = {
                "numproc":      1,
                "numnodes":     1,
                "npool":        900,
                "executable":   "mpirun",
                "params":       "",         # Set already on the foxtrot: "--mca btl openib,sm,self"
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

ZASRLIST            = ZASR.keys()

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

PROCESSORS  = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 24, 36, 48, 60, 72, 84, 96, 108, 120) # ppn = 12

QE_PREFIX   = "'default'"
PREFIX      = "default"
FILDYN      = "matdyn"      # Default name for PH fildyn

MATDYN_METHOD  = OrderedDict()
MATDYN_METHOD["dos"]           = "Phonon Density of States (DOS)"
MATDYN_METHOD["dispersion"]    = "Phonon on Grid (For Virtual Neutron Experiment)"


MATTER_TYPE = OrderedDict()
MATTER_TYPE["metal"]        = "Metal (no gap)"
MATTER_TYPE["insulator"]    = "Insulator (with a gap)"

RELAX       = OrderedDict()
RELAX["relax"]      = "Relaxation (Fixed lattice parameters)"
RELAX["vc-relax"]   = "Variable cell relaxation"

RELAXLIST   = RELAX.keys()

# Example of error message:
# ERROR: masses not defined in PW input file!

__date__ = "$Nov 3, 2009 3:12:34 PM$"


