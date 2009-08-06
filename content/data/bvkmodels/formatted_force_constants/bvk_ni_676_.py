#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=9.74759216207e-26   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 676
reference = 'De Wit, G.A., Brockhouse, B.N.: J. Appl. Phys. 39 (1968) 451'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Ni", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,16.25, 19.39, 0.0, 
                         19.39, 16.25, 0.0, 
                         0.0, 0.0, -0.97 ],
[ 0,0,2.0*a,0.0*a,0.0*a,1.07, 0.0, 0.0, 
                         0.0, 0.056, 0.0, 
                         0.0, 0.0, 0.056 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.963, 0.458, 0.458, 
                         0.458, 0.449, -0.391, 
                         0.458, -0.391, 0.449 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.115, 0.222, 0.0, 
                         0.222, 0.115, 0.0, 
                         0.0, 0.0, -0.457 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.256, -0.072, 0.0, 
                         -0.072, -0.063, 0.0, 
                         0.0, 0.0, -0.04 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
