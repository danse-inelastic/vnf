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

# filediff
NDIF        = 74
SPREAD      = 1
PLANEDIFF   = ("3", "1", "0")

# fileproc
NSTEPS      = "40"
TEMP_S      = "292"
TEMP_F      = "292"
I_TEMP      = False
ITMAX_MOD   = "100"
ERROR_MOD   = "1.e-02"
ITMAX_GRAIN = "100"

__date__ = "$Mar 22, 2011 10:52:10 AM$"


