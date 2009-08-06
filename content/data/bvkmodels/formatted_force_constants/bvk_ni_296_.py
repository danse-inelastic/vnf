#!/usr/bin/python
import System
    
# a scales lattice vectors
a=1.0
m=9.74759216207e-26   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 296
reference = 'Birgenau, R.J., Cordes, J. Dolling, G., Woods, A.D.B.: Phys. Rev. 136 (1964) A 1359'

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
[ 0,0,1.0*a,1.0*a,0.0*a,17.72, 18.735, 0.0, 
                         18.735, 17.72, 0.0, 
                         0.0, 0.0, -1.015 ],
[ 0,0,2.0*a,0.0*a,0.0*a,1.148, 0.0, 0.0, 
                         0.0, -0.998, 0.0, 
                         0.0, 0.0, -0.998 ],
[ 0,0,2.0*a,1.0*a,1.0*a,0.94, 0.253, 0.253, 
                         0.253, 0.182, 0.505, 
                         0.253, 0.505, 0.182 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.459, 0.612, 0.0, 
                         0.612, 0.459, 0.0, 
                         0.0, 0.0, -0.153 ],
[ 0,0,3.0*a,1.0*a,0.0*a,-0.363, -0.174, 0.0, 
                         -0.174, 0.1, 0.0, 
                         0.0, 0.0, 0.158 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
