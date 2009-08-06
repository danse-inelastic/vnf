#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex. 
s3=sqrt(3)
a= s3
c= (4.950000/2.660000)*a
m=1.08585187645e-25   # mass in kg of one atom

lattice_type = "hcp"
temperature = 80    # Units: K
reference = "Chesser, N.J., Axe, J.D.: Phys. Rev. B9 (1974) 4060"

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
  [ 0,1, System.modAxial([ a/s3,0, c/2],   10.150000,[-0.594000,-0.594000,-2.003000]) ],
  [ 1,0, System.modAxial([-a/s3,0,-c/2],   10.150000,[-0.594000,-0.594000,-2.003000]) ],

  [ 0,0, System.modAxial([ 0, a,0],          29.235000,[ -3.484000, -3.484000, -3.347000]) ],
  [ 1,1, System.modAxial([ 0, a,0],          29.235000,[ -3.484000, -3.484000, -3.347000]) ],

  [ 0,1, System.modAxial([-2*a/s3,0, c/2], 3.004000,[ -0.145000, -0.145000, 0.803000]) ],
  [ 1,0, System.modAxial([ 2*a/s3,0,-c/2], 3.004000,[ -0.145000, -0.145000, 0.803000]) ],

  [ 0,0, System.modAxial([ 0,0,c],            0.00,[0.162000,0.162000,-0.075000]) ],
  [ 1,1, System.modAxial([ 0,0,c],            0.00,[0.162000,0.162000,-0.075000]) ],

  [ 0,1, System.modAxial([ 5*a/(2*s3), a/2, c/2],  
                                                -0.353100,[ 0.309000, 0.309000,-0.011000]) ],
  [ 1,0, System.modAxial([-5*a/(2*s3),-a/2,-c/2],  
                                                -0.353100,[ 0.309000, 0.309000,-0.011000]) ],

  [ 0,0, System.modAxial([ a*s3,0,0],        2.264000,[-0.104000,-0.104000,1.051000]) ],
  [ 1,1, System.modAxial([ a*s3,0,0],        2.264000,[-0.104000,-0.104000,1.051000]) ],
  [ 0,0, System.modAxial([-a*s3,0,0],        2.264000,[-0.104000,-0.104000,1.051000]) ],
  [ 1,1, System.modAxial([-a*s3,0,0],        2.264000,[-0.104000,-0.104000,1.051000]) ],

]

System.write(cell,atoms,sites,bonds,"hcp")
