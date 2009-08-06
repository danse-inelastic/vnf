#!/usr/bin/python

import System
from math import sqrt


# a b and c are lattice parameters for hex.  a == b.
a=1.0
b= a
c= (494.0/458.0)*a  # FROM LB.

m=1.9065974e-25

lattice_type = "fct"
temperature = 77    # Units: K
reference = "Smith, H.G., Reichardt, W.: Bull. Am. Phy. Soc. 14 (1969) 378 (unpublished)"

cell=[
  a,b, 0,
  a, 0,c,
   0,b,c
]

atoms=[
  [ "In", m ],
]

sites=[
  [ 0,0,0,             0 ],
]

bonds=[
  [ 0,0, System.axial([  a,   0,  c], 12.316,-2.064) ],
  [ 0,0, System.axial([  a,  b,   0], 16.763,-2.759) ],
  [ 0,0, System.axial([2*a,   0,   0],  1.278, 0.929) ],
  [ 0,0, System.axial([   0,   0,2*c],  1.695, 0.294) ],
  [ 0,0, System.axial([2*a,  b,  c], -0.452, 0.002) ],
  [ 0,0, System.axial([  a,  b,2*c], -0.601, 0.268) ],
  [ 0,0, System.axial([2*a,   0,2*c], -0.423,-0.216) ],
  [ 0,0, System.axial([2*a,2*b,   0], -1.130, 0.033) ],
  [ 0,0, System.axial([3*a,1*b,   0],  0.167, 0.000) ],
  [ 0,0, System.axial([  a,   0,3*c], -0.026, 0.000) ],
  [ 0,0, System.axial([3*a,   0,1*c],  0.225, 0.000) ],
]

System.write(cell,atoms,sites,bonds,"fct")
