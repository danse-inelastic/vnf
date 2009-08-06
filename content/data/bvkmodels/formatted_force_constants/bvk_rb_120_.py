#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=1.41926270342e-25   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 120
reference = 'Copley, J.R.D., Brockhouse, B.N.: Can. J. Phys. 51 (1973) 657'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "Rb", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,0.618, 0.74, 0.74, 
                         0.74, 0.618, 0.74, 
                         0.74, 0.74, 0.618 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.456, 0.0, 0.0, 
                         0.0, 0.012, 0.0, 
                         0.0, 0.0, 0.012 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.034, -0.061, 0.0, 
                         -0.061, -0.034, 0.0, 
                         0.0, 0.0, -0.003 ],
[ 0,0,1.5*a,0.5*a,0.5*a,-0.003, 0.003, 0.003, 
                         0.003, 0.0, 0.004, 
                         0.003, 0.004, 0.0 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
