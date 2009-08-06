#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=3.27078329459e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 295
reference = 'Gilat, G., Nicklow, R.M.: Phys. Rev. 143 (1965) 487'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Au", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,16.61, 19.93, 0.0, 
                         19.93, 16.61, 0.0, 
                         0.0, 0.0, -6.65 ],
[ 0,0,2.0*a,0.0*a,0.0*a,3.95, 0.0, 0.0, 
                         0.0, -1.13, 0.0, 
                         0.0, 0.0, -1.13 ],
[ 0,0,2.0*a,1.0*a,1.0*a,1.0, 0.48, 0.48, 
                         0.48, 0.28, 0.24, 
                         0.48, 0.24, 0.28 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-0.57, -0.36, 0.0, 
                         -0.36, -0.57, 0.0, 
                         0.0, 0.0, -0.21 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.17, -0.06, 0.0, 
                         -0.06, -0.02, 0.0, 
                         0.0, 0.0, 0.0 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
