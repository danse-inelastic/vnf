#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex.
a=sqrt(3)
c=(5.21/3.21)*a
m=4.0359394e-26

lattice_type = "hcp"
temperature = 290    # Units: K
reference = "Singh, S.N., Prakash, S.: Physica 50 (1970) 10 and DeWames, R.E., Wolfram, T., Lehman, G.W.: Phys Rev. 138 (1965) A 717"

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
  [ 0,1, System.axial([ a/sqrt(3),0, c/2],           10.483,-0.309) ],
  [ 1,0, System.axial([-a/sqrt(3),0,-c/2],           10.483,-0.309) ],

  [ 0,0, System.axial([ 0, a,0],                      10.099,-0.292) ],
  [ 1,1, System.axial([ 0, a,0],                      10.099,-0.292) ],

  [ 0,1, System.axial([-2*a/sqrt(3),0, c/2],         -0.222,-0.246) ],
  [ 1,0, System.axial([ 2*a/sqrt(3),0,-c/2],         -0.222,-0.246) ],

  [ 0,0, System.axial([ 0,0,c],                        0.305,-0.490) ],
  [ 1,1, System.axial([ 0,0,c],                        0.305,-0.490) ],

  [ 0,1, System.axial([ 5*a/(2*sqrt(3)), a/2, c/2],  0.748, 0.013) ],
  [ 1,0, System.axial([-5*a/(2*sqrt(3)),-a/2,-c/2],  0.748, 0.013) ],

  [ 0,0, System.axial([ a*sqrt(3),0,0],                0.529, 0.091) ],
  [ 1,1, System.axial([ a*sqrt(3),0,0],                0.529, 0.091) ],
  [ 0,0, System.axial([-a*sqrt(3),0,0],                0.529, 0.091) ],
  [ 1,1, System.axial([-a*sqrt(3),0,0],                0.529, 0.091) ],

  [ 0,0, System.axial([0,a,c],                       -0.049, 0.157) ],
  [ 1,1, System.axial([0,a,c],                       -0.049, 0.157) ],

  [ 0,0, System.axial([0,2*a,0],                      -0.401, 0.042) ],
  [ 1,1, System.axial([0,2*a,0],                      -0.401, 0.042) ],
]

System.write(cell,atoms,sites,bonds,"hcp")
