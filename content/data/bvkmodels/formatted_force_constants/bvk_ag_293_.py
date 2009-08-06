#!/usr/bin/python
import System

# a scales lattice vectors
a=1.0
m=1.79123214879e-25   # mass in kg of one atom
    
lattice_type = 'fcc'
temperature = 293
reference = 'Drexel, W.: Z. Phys. 255 (1972) 281, Drexel, W.: Rep KFK 1383, Kernforschungsanlage Karlsruhe, Germany 1971'

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
[ 0,0,1.0*a,1.0*a,0.0*a,10.4, 12.1, 0.0, 
                         12.1, 10.4, 0.0, 
                         0.0, 0.0, -1.0 ],
[ 0,0,2.0*a,0.0*a,0.0*a,-1.6, 0.0, 0.0, 
                         0.0, -0.5, 0.0, 
                         0.0, 0.0, -0.5 ],
[ 0,0,2.0*a,1.0*a,1.0*a,-0.1, 1.0, 1.0, 
                         1.0, 0.3, 0.0, 
                         1.0, 0.0, 0.3 ],
[ 0,0,2.0*a,2.0*a,0.0*a,0.3, -0.3, 0.0, 
                         -0.3, 0.3, 0.0, 
                         0.0, 0.0, 0.2 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
