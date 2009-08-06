#!/usr/bin/python

# Terbium

import System
from math import sqrt


# a and c are lattice parameters for hex
a=sqrt(3)
c=(5.696/3.599)*a              # Article,  page 3943
# c=(5.70/3.60)*a                  # LB 
m=2.639017e-25           # atomic (average IUPAC) mass in kg

lattice_type = "hcp"
temperature = 298    # Units: K
reference = "Houmann, J.C.G., Nicklow, R.M.: Phys. Rev. B1 (1970) 3943"
details = "The model is axially symmetric from the fifth neighbours outward"

cell=[
  a*sqrt(3)/2,-a/2,0,
  0,a,0,
  0,0,c,
]

atoms=[
  [ "A", m ],
  [ "B", m ],
]

sites=[
  [ 0,0,0,             0 ],
  [ a/sqrt(3),0,c/2, 1 ],
]

bonds=[
  [ 0,1, a/sqrt(3),0,c/2,       5.467, 0.000, 7.286,
                                  0.000, 1.562, 0.000,
                                  7.286, 0.000, 9.901 ],
  [ 1,0,-a/sqrt(3),0,-c/2,      5.467, 0.000, 7.286,
                                  0.000, 1.562, 0.000,
                                  7.286, 0.000, 9.901 ],

# NOTE:  you must take the transpose for Bonds going in the other direction!
  [ 0,0, 0,a,0,                  0.954, 2.426, 0.000,
                                 -2.426,11.416, 0.000,
                                  0.000, 0.000,-0.952 ],
  [ 1,1, 0,a,0,                  0.954,-2.426, 0.000,
                                  2.426,11.416, 0.000,
                                  0.000, 0.000,-0.952 ],

  [ 0,1, -2*a/sqrt(3),0,c/2,   -1.889, 0.000, 0.046,
                                  0.000,-0.975, 0.000,
                                  0.046, 0.000,-0.894 ],
  [ 1,0, 2*a/sqrt(3),0,-c/2,   -1.889, 0.000, 0.046,
                                  0.000,-0.975, 0.000,
                                  0.046, 0.000,-0.894 ],

  [ 0,0, 0,0,c,                 -0.032, 0.000, 0.000,
                                  0.000,-0.032, 0.000,
                                  0.000, 0.000,-2.228 ],
  [ 1,1, 0,0,c,                 -0.032, 0.000, 0.000,
                                  0.000,-0.032, 0.000,
                                  0.000, 0.000,-2.228 ],

  [ 0,1, System.axial([5*a/(2*sqrt(3)),a/2,c/2],    1.225,-0.180) ],
  [ 1,0, System.axial([-5*a/(2*sqrt(3)),-a/2,-c/2], 1.225,-0.180) ],

  [ 0,0, System.axial([ a*sqrt(3),0,0],               1.250, 0.241) ],
  [ 1,1, System.axial([ a*sqrt(3),0,0],               1.250, 0.241) ],
  [ 0,0, System.axial([-a*sqrt(3),0,0],               1.250, 0.241) ],
  [ 1,1, System.axial([-a*sqrt(3),0,0],               1.250, 0.241) ],

  [ 0,0, System.axial([0,a,c],                       0.762,-0.098) ],
  [ 1,1, System.axial([0,a,c],                       0.762,-0.098) ],

  [ 0,0, System.axial([0,2*a,0],                     -0.410, 0.066) ],
  [ 1,1, System.axial([0,2*a,0],                     -0.410, 0.066) ],
]

System.write(cell,atoms,sites,bonds,"hcp")
