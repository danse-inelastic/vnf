#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.05529724344e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 1336
reference = 'Larose, A., Brokchouse, B.N.: Can. J. Phys. 54 (1976) 1990'

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
[ 0,0,1.0*a,1.0*a,0.0*a,11.718, 13.653, 0.0, 
                         13.653, 11.718, 0.0, 
                         0.0, 0.0, -1.787 ],
[ 0,0,2.0*a,0.0*a,0.0*a,0.238, 0.0, 0.0, 
                         0.0, -0.279, 0.0, 
                         0.0, 0.0, -0.279 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.325, 0.153, 0.153, 
                         0.153, 0.095, 0.076, 
                         0.153, 0.076, 0.095 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-0.246, -0.339, 0.0, 
                         -0.339, -0.246, 0.0, 
                         0.0, 0.0, 0.093 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.074, 0.007, 0.0, 
                         0.007, -0.092, 0.0, 
                         0.0, 0.0, -0.095 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
