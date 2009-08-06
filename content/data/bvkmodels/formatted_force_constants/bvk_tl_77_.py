#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex. 
s3=sqrt(3)
a= s3
c= (5.510000/3.450000)*a
m=3.39393889073e-25   # mass in kg of one atom

lattice_type = "hcp"
temperature = 77    # Units: K
reference = "Worlton, T.G., Schmunk, R.E.: Phys. Rev. B3 (1971) 4115"

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
  [ 0,1, System.modAxial([ a/s3,0, c/2],   10.247500,[-1.927800,-1.927800,3.687200]) ],
  [ 1,0, System.modAxial([-a/s3,0,-c/2],   10.247500,[-1.927800,-1.927800,3.687200]) ],

  [ 0,0, System.modAxial([ 0, a,0],          10.540600,[ -0.073300, -0.073300, 0.140200]) ],
  [ 1,1, System.modAxial([ 0, a,0],          10.540600,[ -0.073300, -0.073300, 0.140200]) ],

  [ 0,1, System.modAxial([-2*a/s3,0, c/2], -2.386000,[ 0.860300, 0.860300, -1.645500]) ],
  [ 1,0, System.modAxial([ 2*a/s3,0,-c/2], -2.386000,[ 0.860300, 0.860300, -1.645500]) ],

  [ 0,0, System.modAxial([ 0,0,c],            -1.4887,[-0.252700,-0.252700,0.4833]) ],
  [ 1,1, System.modAxial([ 0,0,c],            -1.4887,[-0.252700,-0.252700,0.4833]) ],

  [ 0,1, System.modAxial([ 5*a/(2*s3), a/2, c/2],  
                                                1.816200,[ 0.031400, 0.031400,-0.060100]) ],
  [ 1,0, System.modAxial([-5*a/(2*s3),-a/2,-c/2],  
                                                1.816200,[ 0.031400, 0.031400,-0.060100]) ],

  [ 0,0, System.modAxial([ a*s3,0,0],        -1.159900,[0.100800,0.100800,-0.193000]) ],
  [ 1,1, System.modAxial([ a*s3,0,0],        -1.159900,[0.100800,0.100800,-0.193000]) ],
  [ 0,0, System.modAxial([-a*s3,0,0],        -1.159900,[0.100800,0.100800,-0.193000]) ],
  [ 1,1, System.modAxial([-a*s3,0,0],        -1.159900,[0.100800,0.100800,-0.193000]) ],

]

System.write(cell,atoms,sites,bonds,"hcp")
