#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=9.74759216207e-26   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 298
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
[ 0,0,1.0*a,1.0*a,0.0*a,17.319, 19.1, 0.0, 
                         19.1, 17.319, 0.0, 
                         0.0, 0.0, -0.436 ],
[ 0,0,2.0*a,0.0*a,0.0*a,1.044, 0.0, 0.0, 
                         0.0, -0.78, 0.0, 
                         0.0, 0.0, -0.78 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.842, 0.424, 0.424, 
                         0.424, 0.263, -0.109, 
                         0.424, -0.109, 0.263 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.402, 0.66, 0.0, 
                         0.66, 0.402, 0.0, 
                         0.0, 0.0, -0.185 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.085, -0.035, 0.0, 
                         -0.035, 0.007, 0.0, 
                         0.0, 0.0, 0.018 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
