#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=1.41926270342e-25   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 85
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
[ 0,0,0.5*a,0.5*a,0.5*a,0.657, 0.746, 0.746, 
                         0.746, 0.657, 0.746, 
                         0.746, 0.746, 0.657 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.4, 0.0, 0.0, 
                         0.0, 0.007, 0.0, 
                         0.0, 0.0, 0.007 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.013, -0.011, 0.0, 
                         -0.011, -0.013, 0.0, 
                         0.0, 0.0, -0.025 ],
[ 0,0,1.5*a,0.5*a,0.5*a,-0.013, -0.002, -0.002, 
                         -0.002, -0.003, -0.027, 
                         -0.002, -0.027, -0.003 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
