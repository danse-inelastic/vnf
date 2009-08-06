#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.05529724344e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 973
reference = 'Larose, A., Brockhouse, B.N.: Can. J. Phys. 54 (1976) 1990'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Cu", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,11.682, 14.384, 0.0, 
                         14.384, 11.682, 0.0, 
                         0.0, 0.0, -1.424 ],
[ 0,0,2.0*a,0.0*a,0.0*a,1.554, 0.0, 0.0, 
                         0.0, 0.074, 0.0, 
                         0.0, 0.0, 0.074 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.658, 0.31, 0.31, 
                         0.31, 0.193, 0.155, 
                         0.31, 0.155, 0.193 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-0.49, -0.466, 0.0, 
                         -0.466, -0.49, 0.0, 
                         0.0, 0.0, -0.024 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.12, -0.022, 0.0, 
                         -0.022, -0.063, 0.0, 
                         0.0, 0.0, -0.055 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
