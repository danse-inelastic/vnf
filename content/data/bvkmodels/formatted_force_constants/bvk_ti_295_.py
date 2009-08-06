#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex. 
s3=sqrt(3)
a= s3
c= (4.680000/2.950000)*a
m=7.94868814347e-26   # mass in kg of one atom

lattice_type = "hcp"
temperature = 295    # Units: K
reference = "Stassis, C., Arch, D., Harmon, B.N., Wakabayashi, N.: Phys. Rev. B19 (1979) 181"

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
  [ 0,1, System.modAxial([ a/s3,0, c/2],   41.380000,[-3.030000,-3.030000,-17.210000]) ],
  [ 1,0, System.modAxial([-a/s3,0,-c/2],   41.380000,[-3.030000,-3.030000,-17.210000]) ],

  [ 0,0, System.modAxial([ 0, a,0],          22.280000,[ 0.171000, 0.171000, 3.780000]) ],
  [ 1,1, System.modAxial([ 0, a,0],          22.280000,[ 0.171000, 0.171000, 3.780000]) ],

  [ 0,1, System.modAxial([-2*a/s3,0, c/2], -8.330000,[ 1.100000, 1.100000, 0.220000]) ],
  [ 1,0, System.modAxial([ 2*a/s3,0,-c/2], -8.330000,[ 1.100000, 1.100000, 0.220000]) ],

  [ 0,0, System.modAxial([ 0,0,c],            0.00,[0.680000,0.680000,12.200000]) ],
  [ 1,1, System.modAxial([ 0,0,c],            0.00,[0.680000,0.680000,12.200000]) ],

  [ 0,1, System.modAxial([ 5*a/(2*s3), a/2, c/2],  
                                                2.260000,[ 0.170000, 0.170000,0.020000]) ],
  [ 1,0, System.modAxial([-5*a/(2*s3),-a/2,-c/2],  
                                                2.260000,[ 0.170000, 0.170000,0.020000]) ],

  [ 0,0, System.modAxial([ a*s3,0,0],        0.650000,[1.510000,1.510000,0.230000]) ],
  [ 1,1, System.modAxial([ a*s3,0,0],        0.650000,[1.510000,1.510000,0.230000]) ],
  [ 0,0, System.modAxial([-a*s3,0,0],        0.650000,[1.510000,1.510000,0.230000]) ],
  [ 1,1, System.modAxial([-a*s3,0,0],        0.650000,[1.510000,1.510000,0.230000]) ],

]

System.write(cell,atoms,sites,bonds,"hcp")
