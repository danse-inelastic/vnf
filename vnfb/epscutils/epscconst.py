# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from vnfb.utils.orderedDict import OrderedDict

NUMPROC = 1 # Number of thermo-mechanical processes

FILETYPE    = ("filecrys", "filesamp", "filediff", "fileproc")
EPSC_BIN    = "epsc3"       # Binary for EPSC should be epsc3
EPSC_IN     = "epsc3.in"    # Filename for main config file
EPSC_OUT    = "EPSC.out"    # Filename for output file
EPSC_OUT_RE = "EPSC\.out$"  # Regular expression for output file

EPSC_OUT_FILES = [EPSC_OUT, "epsc1.out", "epsc2.out", "epsc3.out", "epsc4.out",
                  "epsc5.out", "epsc6.out", "epsc7.out", "epsc8.out",
                  "epsc9.out", "epsc10.out", "epsc11.out", "epsc12.out",
                  "epsc13.out", "epsc14.out", "epsc15.out"]

EPSC_OUT_TIPS = ["Main output",
                "File for sample and convergence",
                "File for grains state and plastic activity",
                "Components 11 22 33 of sample strain, stress, elastic  strain and avacs",
                "Final sample and grains state",
                "Evolution of sample strain rate, strain (and devs)",
                "Evolution of sample stress rate, stress (and devs)",
                "Relative activity in each mode and avacs vs strain",
                "Equivalent states",
                "Evolution of internal strains", "", "", "", "", "", ""]


EPSCCHAIN   = OrderedDict()
EPSCCHAIN["epsc"]   = ("epsc",)

TYPE_DESC   = OrderedDict()
TYPE_DESC[FILETYPE[0]]  = "Material"        # filecrys
TYPE_DESC[FILETYPE[1]]  = "Sample"          # filesamp
TYPE_DESC[FILETYPE[2]]  = "Diffraction"     # filediff
TYPE_DESC[FILETYPE[3]]  = "Process"         # fileproc

# filecrys
CRYSYM  = ("CUBIC", "HEXAG")
LATTICE = ("3.5", "3.5", "3.5", "90", "90", "90") # Temp
CCC2    = """  0.899E+02  0.683E+02  0.683E+02  0.000E+00  0.000E+00  0.000E+00
  0.683E+02  0.899E+02  0.683E+02  0.000E+00  0.000E+00  0.000E+00
  0.683E+02  0.683E+02  0.899E+02  0.000E+00  0.000E+00  0.000E+00
  0.000E+00  0.000E+00  0.000E+00  0.327E+02  0.000E+00  0.000E+00
  0.000E+00  0.000E+00  0.000E+00  0.000E+00  0.327E+02  0.000E+00
  0.000E+00  0.000E+00  0.000E+00  0.000E+00  0.000E+00  0.327E+02"""

ALFACC  = ("10.0e-6", "10.0e-6", "10.0e-6", "0", "0", "0")
NMODESX = (1,)
NAMESYS = "<111>{110} SLIP"
MODEX   = """ 1  12  20   1                           modex,nsmx,nrsx,iopsysx
 0.000   0.000   0.000   0.000           stw,twvol,gamdthr,tauprop
 0.075   0.365   32.5    1.300           tau0,tau1,thet0,thet1 (Voce hard)
 1.0   1.0   1.0                         hself,hlat(nmodes)
   1  1 -1        0  1  1
   1  1 -1        1  0  1
   1  1 -1        1 -1  0
   1 -1 -1        0  1 -1
   1 -1 -1        1  0  1
   1 -1 -1        1  1  0
   1 -1  1        0  1  1
   1 -1  1        1  0 -1
   1 -1  1        1  1  0
   1  1  1        0  1 -1
   1  1  1        1  0 -1
   1  1  1        1 -1  0"""

FILECRYS_T = """*Material: 
%s           crysym
   %s   %s   %s   %s   %s   %s   unit cell axes and angles
Elastic stiffness (single crystal [GPa]; scaled=0.85xINTERPOLATED)
%s
*Thermal expansion coefficients (single crystal in crystal axis):
 %s  %s  %s   %s   %s   %s                    "alfacc"
*Info about slip & twinning modes in this file:
  %s          nmodesx    (total # of modes listed in file)
  %s          nmodes     (# of modes to be used in the calculation)
  1          mode(i)    (label of the modes to be used)
  %s
%s"""


# filesamp
ELLIPSOID   = ("1.0", "1.0", "1.0")
NGRAIN      = "1000"

FILESAMP_T  = """AXES OF THE REPRESENTATIVE ELLIPSOID
	%s	%s	%s
DISCRETE TEXTURE FROM ODF FILE
B	%s	0
%s
"""

# filediff
NDIF        = 74
SPREAD      = 1
PLANEDIFF   = ("3", "1", "0")

FILEDIFF_T  = """*DIFFRACTING PLANES AND DIRECTION
*Number of diffraction directions and diffracting angle spread:
  %s  %s					"ndif"	"spread"
*Plane type and direction angle:
*"n3" or "n4"   "theta"        "phi"
%s
"""

# fileproc
NSTEPS      = "40"
TEMP_S      = "292"
TEMP_F      = "292"
I_TEMP      = False
ITMAX_MOD   = "100"
ERROR_MOD   = "1.e-02"
ITMAX_GRAIN = "100"

FILEPROC_T  = """* Thermo-mechanical process
*Number of steps in the process:
%s								"nsteps"
*Starting and final temperature:
%s  %s						"temp_s" "temp_f"
*Enforced temperature dependence of elastic constants (1=YES or 0=NO)?
%s                                                                 "i_temp_cij"
*Indexes and values for the stress boundary condition:
	0	1	1	1	1	1			"istbd"
	999	0.0	0.0	0.0	0.0	0.0			"stbc"
*Indexes and values for the strain boundary condition:
	1	0	0	0	0	0			"ietbc"
	-0.03	999   999	999	999	999			"etbc"
*Reset macroscopic strain to zero (1=YES or 0=NO)?
1
*Control process variable: 0=temp , 1,2,3=etss(1,2,3) , 4,5,6=stss(1,2,3)
1									"i_control_var"
*Convergence criterium for the sample moduli:
%s  %s                                           "itmax_mod"  "error_mod"
*Maximum number of iterations to select the set of systems in grains:
%s                                            "itmax_grain"
"""

EPSC_IN_TEXT = """* Main configuration file
*File for the material data:
filecrys
*File for the sample (grain shape+texture) data:
filesamp
*Reads state from previous process (1=YES or 0=NO) and related file:
0                                                                "i_prev_proc"
* 
*Reads diffracting planes and diffraction directions (1=YES or 0=NO) and file:
1                                                                 "i_diff_dir"
filediff
*Number of thermomechanical processes to be run:
1                                                                     "nproc"
*Files containing information about each process:
fileproc
"""

__date__ = "$Mar 22, 2011 10:52:10 AM$"


