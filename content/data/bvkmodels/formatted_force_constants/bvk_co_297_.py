#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=9.78631683826e-26   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 297
reference = 'Svensson, E.C., Powell, B.M., Woods, A.D.B., Teuchert, W-D.: Can J. Phys. 57 (1979) 253'

cell=[
  a,a,0,
  a,0,a,
  0,-a,-a
]

atoms=[
  [ "Co", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,1.0*a,1.0*a,0.0*a,15.71, 18.77, 0.0, 
                         18.77, 15.71, 0.0, 
                         0.0, 0.0, 0.27 ],
[ 0,0,2.0*a,0.0*a,0.0*a,0.32, 0.0, 0.0, 
                         0.0, 0.27, 0.0, 
                         0.0, 0.0, 0.27 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.36, 0.27, 0.27, 
                         0.27, -0.2, 0.38, 
                         0.27, 0.38, -0.2 ],
[ 0,0,2.0*a,2.0*a,0.0*a,1.52, 1.36, 0.0, 
                         1.36, 1.52, 0.0, 
                         0.0, 0.0, 0.09 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
