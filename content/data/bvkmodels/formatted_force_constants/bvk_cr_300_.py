#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=8.63434075058e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 300
reference = 'Shaw, W.M., Muhlestein, L.D.: Phys. Rev. B4 (1971) 969.'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "Cr", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,13.526, 6.487, 6.487, 
                         6.487, 13.526, 6.487, 
                         6.487, 6.487, 13.526 ],
[ 0,0,1.0*a,0.0*a,0.0*a,35.915, 0.0, 0.0, 
                         0.0, -1.564, 0.0, 
                         0.0, 0.0, -1.564 ],
[ 0,0,1.0*a,1.0*a,0.0*a,2.042, 2.871, 0.0, 
                         2.871, 2.042, 0.0, 
                         0.0, 0.0, -0.05 ],
[ 0,0,1.5*a,0.5*a,0.5*a,-1.257, 0.007, 0.007, 
                         0.007, 0.432, 0.516, 
                         0.007, 0.516, 0.432 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
