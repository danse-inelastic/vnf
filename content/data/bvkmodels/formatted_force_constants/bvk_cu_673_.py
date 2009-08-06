#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.05529724344e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 673
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
[ 0,0,1.0*a,1.0*a,0.0*a,12.275, 14.062, 0.0, 
                         14.062, 12.275, 0.0, 
                         0.0, 0.0, -1.321 ],
[ 0,0,2.0*a,0.0*a,0.0*a,0.696, 0.0, 0.0, 
                         0.0, -0.355, 0.0, 
                         0.0, 0.0, -0.355 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.744, 0.331, 0.331, 
                         0.331, -0.246, 0.185, 
                         0.331, 0.185, -0.246 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-0.174, -0.15, 0.0, 
                         -0.15, -0.174, 0.0, 
                         0.0, 0.0, -0.024 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.19, -0.041, 0.0, 
                         -0.041, -0.08, 0.0, 
                         0.0, 0.0, -0.067 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
