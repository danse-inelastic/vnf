#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=3.05280637662e-25   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 298
reference = 'Larose, A., Brockhouse, B.N.: Can. J. Phys. 54 (1976) 1819'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "W", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,22.1, 18.9, 18.9, 
                         18.9, 22.1, 18.9, 
                         18.9, 18.9, 22.1 ],
[ 0,0,1.0*a,0.0*a,0.0*a,45.7, 0.0, 0.0, 
                         0.0, 0.7, 0.0, 
                         0.0, 0.0, 0.7 ],
[ 0,0,1.0*a,1.0*a,0.0*a,3.7, 5.2, 0.0, 
                         5.2, 3.7, 0.0, 
                         0.0, 0.0, -1.3 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
