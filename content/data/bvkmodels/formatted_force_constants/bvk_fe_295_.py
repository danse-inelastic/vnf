#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=9.27266688808e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 295
reference = 'Minkiewicz, V.J., Shirane, G., Nathans, R.: Phys. Rev. 162 (1967) 528'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "Fe", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,16.88, 15.01, 15.01, 
                         15.01, 16.88, 15.01, 
                         15.01, 15.01, 16.88 ],
[ 0,0,1.0*a,0.0*a,0.0*a,14.63, 0.0, 0.0, 
                         0.0, 0.55, 0.0, 
                         0.0, 0.0, 0.55 ],
[ 0,0,1.0*a,1.0*a,0.0*a,0.92, 0.69, 0.0, 
                         0.69, 0.92, 0.0, 
                         0.0, 0.0, -0.57 ],
[ 0,0,1.5*a,0.5*a,0.5*a,-0.12, 0.007, 0.007, 
                         0.007, 0.03, 0.52, 
                         0.007, 0.52, 0.03 ],
[ 0,0,1.0*a,1.0*a,1.0*a,-0.29, 0.32, 0.32, 
                      0.32, -0.29, 0.32, 
                      0.32, 0.32, -0.29 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
