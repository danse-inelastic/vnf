#!/usr/bin/python

import System
from math import sqrt


# a and c are lattice parameters for hex. 
s3=sqrt(3)
a= s3
c= (5.510000/3.450000)*a
m=3.39393889073e-25   # mass in kg of one atom

lattice_type = "hcp"
temperature = 296    # Units: K
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
  [ 0,1, System.modAxial([ a/s3,0, c/2],   15.491100,[-2.421600,-2.421600,-3.782400]) ],
  [ 1,0, System.modAxial([-a/s3,0,-c/2],   15.491100,[-2.421600,-2.421600,-3.782400]) ],

  [ 0,0, System.modAxial([ 0, a,0],          12.870400,[ -1.157100, -1.157100, -1.807300]) ],
  [ 1,1, System.modAxial([ 0, a,0],          12.870400,[ -1.157100, -1.157100, -1.807300]) ],

  [ 0,1, System.modAxial([-2*a/s3,0, c/2], -0.481900,[ 0.608800, 0.608800, -0.950900]) ],
  [ 1,0, System.modAxial([ 2*a/s3,0,-c/2], -0.481900,[ 0.608800, 0.608800, -0.950900]) ],

  [ 0,0, System.modAxial([ 0,0,c],            -0.8846,[0.078500,0.078500,0.1226]) ],
  [ 1,1, System.modAxial([ 0,0,c],            -0.8846,[0.078500,0.078500,0.1226]) ],

  [ 0,1, System.modAxial([ 5*a/(2*s3), a/2, c/2],  
                                                -0.295500,[ 0.177400, 0.177400,0.277100]) ],
  [ 1,0, System.modAxial([-5*a/(2*s3),-a/2,-c/2],  
                                                -0.295500,[ 0.177400, 0.177400,0.277100]) ],

  [ 0,0, System.modAxial([ a*s3,0,0],        -0.321200,[-0.274800,-0.274800,-0.429200]) ],
  [ 1,1, System.modAxial([ a*s3,0,0],        -0.321200,[-0.274800,-0.274800,-0.429200]) ],
  [ 0,0, System.modAxial([-a*s3,0,0],        -0.321200,[-0.274800,-0.274800,-0.429200]) ],
  [ 1,1, System.modAxial([-a*s3,0,0],        -0.321200,[-0.274800,-0.274800,-0.429200]) ],

]

System.write(cell,atoms,sites,bonds,"hcp")
