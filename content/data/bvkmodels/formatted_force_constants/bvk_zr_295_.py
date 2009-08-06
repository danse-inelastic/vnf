#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex. ## I think.  double check "s3"
s3=sqrt(3)
a= s3
c= (5.14/3.23)*a
m=1.5148099e-25

lattice_type = "hcp"
temperature = 295   # Units: K
reference = "Stassis, C., Zarestky, J., Arch, D., McMasters, O.D., Harmon, B.N.: Phys. Rev. B18 (1978) 2632"

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
  [ a/s3,0,c/2,     1 ],
]

bonds=[
  [ 0,1, System.modAxial([ a/s3,0, c/2],   39.74,[-3.77,-3.77,-12.88]) ],
  [ 1,0, System.modAxial([-a/s3,0,-c/2],   39.74,[-3.77,-3.77,-12.88]) ],

  [ 0,0, System.modAxial([ 0, a,0],          22.80,[-0.70,-0.70,  3.28]) ],
  [ 1,1, System.modAxial([ 0, a,0],          22.80,[-0.70,-0.70,  3.28]) ],

  [ 0,1, System.modAxial([-2*a/s3,0, c/2], -4.60,[-0.39,-0.39, -1.45]) ],
  [ 1,0, System.modAxial([ 2*a/s3,0,-c/2], -4.60,[-0.39,-0.39, -1.45]) ],

  [ 0,0, System.modAxial([ 0,0,c],            4.40,[ 0.43, 0.43,  4.00]) ],
  [ 1,1, System.modAxial([ 0,0,c],            4.40,[ 0.43, 0.43,  4.00]) ],

  [ 0,1, System.modAxial([ 5*a/(2*s3), a/2, c/2],  
                                                1.95,[ 0.28, 0.28, -0.26]) ],
  [ 1,0, System.modAxial([-5*a/(2*s3),-a/2,-c/2],  
                                                1.95,[ 0.28, 0.28, -0.26]) ],

  [ 0,0, System.modAxial([ a*s3,0,0],        1.48,[ 1.71, 1.71,  0.10]) ],
  [ 1,1, System.modAxial([ a*s3,0,0],        1.48,[ 1.71, 1.71,  0.10]) ],
  [ 0,0, System.modAxial([-a*s3,0,0],        1.48,[ 1.71, 1.71,  0.10]) ],
  [ 1,1, System.modAxial([-a*s3,0,0],        1.48,[ 1.71, 1.71,  0.10]) ],

]

System.write(cell,atoms,sites,bonds,"hcp")
