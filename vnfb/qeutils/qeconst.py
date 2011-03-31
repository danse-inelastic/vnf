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

# XXX: Refactor TYPE dictionary to extend associated information
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
               "D3":        "d3.x",
               "CP":        "cp.x",
               "CPPP":      "cppp.x"
               }
               # Other types: "INITIAL_STATE", "GIPAW", "D1", "PROJWFC", "PWCOND"

# XXX: Revise the tips according to
TYPETIP     = {"PW":        "Plane wave calculation",
               "PH":        "Phonon calculation",
               "BANDS":     "Bands structure calculation",
               "PLOTBAND":  "Plot bands post processing",
               "PP":        "Post processing",
               "DOS":       "Electronic Density of States (DOS) calculation",
               "Q2R":       "Fourier transform to real space",
               "MATDYN":    "Dynamical matrix calculation",
               "DYNMAT":    "Dynamical matrix calculation",
               "D3":        "Third-order derivative calculation",
               "CP":        "Car-Parrinello molecular dynamics",
               "CPPP":      "Car-Parrinello molecular dynamics post processing"
               }


INPUT_EXT   = ".in"
OUTPUT_EXT  = ".out"

INPUT           = OrderedDict()
INPUT["pw"]     = "pw"      + INPUT_EXT
INPUT["ph"]     = "ph"      + INPUT_EXT
INPUT["bands"]  = "bands"   + INPUT_EXT
INPUT["pp"]     = "pp"      + INPUT_EXT
INPUT["dos"]    = "dos"     + INPUT_EXT
INPUT["q2r"]    = "q2r"     + INPUT_EXT
INPUT["matdyn"] = "matdyn"  + INPUT_EXT
INPUT["dynmat"] = "dynmat"  + INPUT_EXT
INPUT["d3"]     = "d3"      + INPUT_EXT
INPUT["cp"]     = "cp"      + INPUT_EXT
INPUT["cppp"]   = "cppp"    + INPUT_EXT
INPUT["plotband"]   = "plotband"    + INPUT_EXT
INPUT_DEFAULT   = "default" + INPUT_EXT

NOPARALLEL  = ("DOS", "MATDYN", "DYNMAT", "Q2R", "PLOTBAND", "trajectory") # "PP"? # "PLOTBAND"?

NOPARALSIM  = ("single-phonon",)    # List of simulation types each of the tasks should run on single core

# Notes:
#   - "BANDS" is a parallel program (should run on the same number of cores as PW task)
#   - "DYNMAT" is not a parallel program

# List of possible orders
LINKORDER               = OrderedDict()
LINKORDER["PW"]         = None  # No definitive order (options: 0, 1)
LINKORDER["CP"]         = None  # No definitive order (options: 0, 1, 2, 3, 4, 5)
LINKORDER["CPPP"]       = None
LINKORDER["PH"]         = 1
LINKORDER["DYNMAT"]     = 2
LINKORDER["Q2R"]        = 2
LINKORDER["DOS"]        = 2
LINKORDER["BANDS"]      = 2
LINKORDER["MATDYN"]     = 3
LINKORDER["PLOTBAND"]   = 3


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
SIMTYPE["molecular-dynamics"]   = "Molecular Dynamics"  # Don't change for now!

# Types of simulations
SIMCHAINS   = OrderedDict()
SIMCHAINS[SIMTYPE["scf"]]                   = ("PW",)
SIMCHAINS[SIMTYPE["electron-dos"]]          = ("PW", "PW", "DOS")
SIMCHAINS[SIMTYPE["electron-dispersion"]]   = ("PW", "PW", "BANDS", "PLOTBAND")
SIMCHAINS[SIMTYPE["geometry"]]              = ("PW",)
SIMCHAINS[SIMTYPE["single-phonon"]]         = ("PW", "PH", "DYNMAT")
SIMCHAINS[SIMTYPE["multiple-phonon"]]       = ("PW", "PH", "Q2R", "MATDYN") # DOS and Dispersion, See: example06
SIMCHAINS[SIMTYPE["molecular-dynamics"]]    = ("CP", "CPPP")  # Default chain, user defined chain is normally used

SIMLIST     = SIMTYPE.values()

# For cp.x (Car-Parrinello molecular dynamics) simulation only
MDSTEPS     = OrderedDict()
MDSTEPS["electron-min"] = "Electronic Minimization"
MDSTEPS["ion-min"]      = "Ion Minimization"
MDSTEPS["ion-random"]   = "Ions Randomization"
MDSTEPS["quenching"]    = "Electrons and Ions Quenching"
MDSTEPS["dynamics"]     = "Electron and Ion Dynamics"
MDSTEPS["thermostat"]   = "Electron and Ion Dynamics with Nose Thermostat"
MDSTEPS["trajectory"]   = "Trajectory Analysis"

# XXX: Get rid of repetition
MDLABEL     = OrderedDict()
MDLABEL["electron-min"] = ("Electronic Minimization", "Electronic minimization with fixed ions and cells")
MDLABEL["ion-min"]      = ("Ion Minimization", "Ion minimization with damped electron dynamics and fixed cells")
MDLABEL["ion-random"]   = ("Ions Randomization", "Ions randomization")
MDLABEL["quenching"]    = ("Quenching", "Electrons and ions quenching")
MDLABEL["dynamics"]     = ("Electron and Ion Dynamics", "Electron and ion dynamics with fixed cells")
MDLABEL["thermostat"]   = ("Dynamics with Thermostat", "Electrons and ions dynamics with Nose thermostat")
MDLABEL["trajectory"]   = ("Trajectory Analysis", "Trajectory analysis")

MDPLOT      = OrderedDict()
MDPLOT["vdos"]          = "Vibrational Density of States (VDOS)"
MDPLOT["vdist"]         = "Velocity Distribution"
MDPLOT["msd"]           = "Mean-Square Displacement"
MDPLOT["rdf"]           = "Radial Distribution Function"
MDPLOT["temptime"]      = "Temperature Dependence on Time"

QETYPES = TYPE.keys() + MDSTEPS.keys()

# Analysis actors
ANALYSIS    = OrderedDict()
ANALYSIS[SIMLIST[0]]    = "electron"
ANALYSIS[SIMLIST[1]]    = "electron-dos"
ANALYSIS[SIMLIST[2]]    = "electron-dispersion"
ANALYSIS[SIMLIST[3]]    = "geometry"
ANALYSIS[SIMLIST[4]]    = "phonon-single"
ANALYSIS[SIMLIST[5]]    = "phonon-multiple"
ANALYSIS[SIMLIST[6]]    = "molecular-dynamics"

#ANALYSIS_ACTORS = ANALYSIS

def coresList(cpn, nodes):
    """
    Populates list of available number of cores based on number of nodes
    and cores per node
    
    General formula:
    servers   = dds.getServers(id=<someid>)   # Get server record
    cpn       = servers.corespernode  # Cores per node
    nodes     = servers.nodes         # Number of nodes
    """
    return [i for i in range(1,cpn+1)]+[i*cpn for i in range(2,nodes+1)]


# XXX: Move to configuration file
# List of number of cores available
SERVERS     = OrderedDict()
SERVERS["foxtrot"] = {  "id":           "server003",
                        "name":         "foxtrot.danse.us",
                        "coreslist":    coresList(12, 34),
                        "opt":          True,
                        "optmsg":       "Foxtrot message"}
                        
SERVERS["octopod"] = {  "id":           "server001",
                        "name":         "octopod.danse.us",
                        "coreslist":    coresList(32, 1),
                        "opt":          False,   # No optimization
                        "optmsg":       "Octopod message"}


# Torque states
TORQUE_STATES = {
        'C': 'finished',
        'R': 'running',
        'Q': 'queued',
        'E': 'exiting', # intermediate state, Running -> Exiting -> Completed
        'H': 'onhold',  # cancelled
        'T': 'moved',
        'W': 'waiting',
        'S': 'suspend', # stopped
        }


# Job states
JOB_STATE   = OrderedDict()

# Job submitting to cluster:      (percentage, description)
JOB_STATE["create-job"]         = (10, "Creating job record ...")
JOB_STATE["prepare-configs"]    = (20, "Preparing configuration files ...")
JOB_STATE["prepare-controls"]   = (40, "Preparing control files ...")
JOB_STATE["copy-files"]         = (60, "Copying files to cluster ...")
JOB_STATE["enqueue"]            = (80, "Submitting to queue ...")
JOB_STATE["submitted"]          = (100, "Done!")
JOB_STATE["submit-failed"]      = (100, "Submit failed! :(")

# Job on cluster (Torque states: taken from vnfb.clusterscheduler.torque._states)
JOB_STATE["finished"]           = "finished"
JOB_STATE["running"]            = "running"
JOB_STATE["queued"]             = "queued"
JOB_STATE["exiting"]            = "exiting"
JOB_STATE["onhold"]             = "onhold"
JOB_STATE["moved"]              = "moved"
JOB_STATE["waiting"]            = "waiting"
JOB_STATE["suspend"]            = "suspend"

# Misc
JOB_STATE["none"]               = "None"

PARSERS   = ("qeinput",)

# XXX: Server specific
# Settings specific for QE and foxtrot
SETTINGS  = {
                "numproc":      1,
                "numnodes":     1,
                "npool":        900,
                "executable":   "mpirun",
                "params":       "",    
                "modules":      ""    
              }

# Default name of script that runs simulation of computing cluster
RUNSCRIPT   = "run.sh"

RESULTS_ID      = "results-link"
ID_SIMTASKS     = "qe-simchain"
ID_OUTPUT       = "qe-container-output"
ID_STATUS       = "qe-container-status"
ID_CONV_JOBS    = "qe-convergence-jobs"
ID_CONV_OPT     = "qe-convergence-optimal"
ID_MD_OPTIONS   = "qe-md-options"
ID_MD_LABEL     = "qe-md-label"
TASK_ACTION     = "task-action"

# Convergence parameter ids
ID_START    = "formtextfield-start"
ID_STEP     = "formtextfield-step"
ID_PARAM    = "formselectorfield-param"

# Settings form
ID_SELECTOR_CORES   = "selector-cores"

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

QE_PREFIX   = "'default'"
PREFIX      = "default"
FILDYN      = "matdyn"      # Default name for PH fildyn

SUBTYPE_MATDYN  = ("dos", "dispersion")

# Depricate?
MATDYN_METHOD  = OrderedDict()
MATDYN_METHOD["dos"]           = "Phonon Density of States (DOS)"
MATDYN_METHOD["dispersion"]    = "Phonon on Grid (For Virtual Neutron Experiment)"


MATDYN_METHOD_LIST  = MATDYN_METHOD.keys()

MATTER_TYPE = OrderedDict()
MATTER_TYPE["metal"]        = "Metal (no gap)"
MATTER_TYPE["insulator"]    = "Insulator (with a gap)"

RELAX       = OrderedDict()
RELAX["relax"]      = "Relaxation (Fixed lattice parameters)"
RELAX["vc-relax"]   = "Variable cell relaxation"

RELAXLIST   = RELAX.keys()

FILBAND     = "'bands.dat'"  # Default value for 'filband' parameter of bands.x calculation

# Example of error message:
# ERROR: masses not defined in PW input file!

# Convergence parameters (from PW config input)
# Format: (OPERAND, TYPE, START, STEP)
CONVPARAM   = OrderedDict()
#CONVPARAM["nbnd"]       = ("add", "int", 2, 1) # Subtle parameter
CONVPARAM["degauss"]    = ("add", "double", 0.05, -0.005)
CONVPARAM["ecutwfc"]    = ("add", "double", 16, 4)
CONVPARAM["ecutrho"]    = ("add", "double", 64, 16)
CONVPARAM["conv_thr"]   = ("multiply", "double", 1e-6, 0.1)
CONVPARAM["kpoints"]    = ("add", "vector", "8, 8, 8", "2, 2, 2")

CONVPARAMLIST   = CONVPARAM.keys()

# Criteria according to which the the convergence occurs
CONVTYPE    = OrderedDict()
CONVTYPE["total-energy"]    = "Total Energy"
CONVTYPE["fermi-energy"]    = "Fermi Energy"
CONVTYPE["frequency"]       = "Single Phonon Frequencies"

CONVTYPELIST    = CONVTYPE.keys()

# Convergence default parameters
MAX_STEPS   = 10
TOLERANCE   = 1.0

# Optimization parameters
OPT_DEFAULT = False

# Generator types 
GENERATOR_TYPES  = ("pw",
                    "ph",
                    "bands",
                    "plotband",
                    "dos",
                    "q2r",
                    "matdyn",
                    "dynmat",
                    "electron-min",
                    "ion-min",
                    "ion-random",
                    "quenching",
                    "dynamics",
                    "thermostat",
                    "trajectory")


__date__ = "$Nov 3, 2009 3:12:34 PM$"


