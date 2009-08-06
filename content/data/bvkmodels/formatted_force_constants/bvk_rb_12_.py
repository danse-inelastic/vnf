#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=1.41926270342e-25   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 12
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
[ 0,0,0.5*a,0.5*a,0.5*a,0.669, 0.788, 0.788, 
                         0.788, 0.669, 0.788, 
                         0.788, 0.788, 0.669 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.397, 0.0, 0.0, 
                         0.0, 0.022, 0.0, 
                         0.0, 0.0, 0.022 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.037, 0.043, 0.0, 
                         0.043, -0.037, 0.0, 
                         0.0, 0.0, -0.009 ],
[ 0,0,1.5*a,0.5*a,0.5*a,0.018, -0.009, -0.009, 
                         -0.009, -0.004, -0.01, 
                         -0.009, -0.01, -0.004 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
