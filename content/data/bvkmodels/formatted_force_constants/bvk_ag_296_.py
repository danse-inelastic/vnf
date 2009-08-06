#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=1.79123214879e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 296
reference = 'Kamitakahara, W.A., Brockhouse, B.N.: Phys. Lett. 29A (1969) 639'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Ag", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,10.71, 12.32, 0.0, 
                         12.32, 10.71, 0.0, 
                         0.0, 0.0, 1.75 ],
[ 0,0,2.0*a,0.0*a,0.0*a,0.06, 0.0, 0.0, 
                         0.0, -0.23, 0.0, 
                         0.0, 0.0, -0.23 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.52, 0.3, 0.3, 
                         0.3, 0.21, 0.05, 
                         0.3, 0.05, 0.21 ],
[ 0,0,2.0*a,2.0*a,0.0*a,-0.13, -0.14, 0.0, 
                         -0.14, -0.13, 0.0, 
                         0.0, 0.0, 0.01 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
