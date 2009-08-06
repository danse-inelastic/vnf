#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=8.45931584191e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 296
reference = 'Cohen, M., Heine, V., Weaire, D.: Solid State Phys. (H. Ehrenreich, F. Seitz and D. Turnbull eds.) Academic Press, New York 24 (1970)'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "V", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,10.534, 6.305, 6.305, 
                         6.305, 10.534, 6.305, 
                         6.305, 6.305, 10.534 ],
[ 0,0,1.0*a,0.0*a,0.0*a,7.129, 0.0, 0.0, 
                         0.0, -0.955, 0.0, 
                         0.0, 0.0, -0.955 ],
[ 0,0,1.0*a,1.0*a,0.0*a,2.73, 0.952, 0.0, 
                         0.952, 2.73, 0.0, 
                         0.0, 0.0, -4.494 ],
[ 0,0,1.5*a,0.5*a,0.5*a,1.555, 0.977, 0.977, 
                         0.977, 0.42, -1.527, 
                         0.977, -1.527, 0.42 ],
[ 0,0,1.0*a,1.0*a,1.0*a,-0.296, 0.263, 0.263, 
                      0.263, -0.296, 0.263, 
                      0.263, 0.263, -0.296 ],
[ 0,0,2.0*a,0.0*a,0.0*a,-1.389, 0.0, 0.0, 
                      0.0, 0.66, 0.0, 
                      0.0, 0.0, 0.66 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
