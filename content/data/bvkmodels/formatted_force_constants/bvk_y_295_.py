#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex. 
s3=sqrt(3)
a= s3
c= (5.730000/3.650000)*a
m=1.47635337097e-25   # mass in kg of one atom

lattice_type = "hcp"
temperature = 295    # Units: K
reference = "Sinha, S.K., Brun, T.O., Muhlestein, L.D., Sakurai, J.: Phys. Rev. B 1 (1970) 2430"

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
  [ 0,1, System.modAxial([ a/s3,0, c/2],   23.239000,[-1.628000,-1.628000,-3.641000]) ],
  [ 1,0, System.modAxial([-a/s3,0,-c/2],   23.239000,[-1.628000,-1.628000,-3.641000]) ],

  [ 0,0, System.modAxial([ 0, a,0],          10.124000,[ 1.456000, 1.456000, 0.150000]) ],
  [ 1,1, System.modAxial([ 0, a,0],          10.124000,[ 1.456000, 1.456000, 0.150000]) ],

  [ 0,1, System.modAxial([-2*a/s3,0, c/2], -6.393000,[ 1.212000, 1.212000, 1.511000]) ],
  [ 1,0, System.modAxial([ 2*a/s3,0,-c/2], -6.393000,[ 1.212000, 1.212000, 1.511000]) ],

  [ 0,0, System.modAxial([ 0,0,c],            0.00,[-0.178000,-0.178000,-0.083000]) ],
  [ 1,1, System.modAxial([ 0,0,c],            0.00,[-0.178000,-0.178000,-0.083000]) ],

  [ 0,1, System.modAxial([ 5*a/(2*s3), a/2, c/2],  
                                                1.392000,[ 0.456000, 0.456000,-0.582000]) ],
  [ 1,0, System.modAxial([-5*a/(2*s3),-a/2,-c/2],  
                                                1.392000,[ 0.456000, 0.456000,-0.582000]) ],

  [ 0,0, System.modAxial([ a*s3,0,0],        1.856000,[-0.093000,-0.093000,0.593000]) ],
  [ 1,1, System.modAxial([ a*s3,0,0],        1.856000,[-0.093000,-0.093000,0.593000]) ],
  [ 0,0, System.modAxial([-a*s3,0,0],        1.856000,[-0.093000,-0.093000,0.593000]) ],
  [ 1,1, System.modAxial([-a*s3,0,0],        1.856000,[-0.093000,-0.093000,0.593000]) ],

]

System.write(cell,atoms,sites,bonds,"hcp")
