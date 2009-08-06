#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=3.81766854865e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 90
reference = 'Woods, A.D.B., Brockhouse, B.N., March, R.H., Stewart, A.T., Bowers, R.: Phys. Rev. 128 (1962) 1112'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "Na", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,1.178, 1.132, 1.132, 
                         1.132, 1.178, 1.132, 
                         1.132, 1.132, 1.178 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.472, 0.0, 0.0, 
                         0.0, 0.104, 0.0, 
                         0.0, 0.0, 0.104 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.038, -0.065, 0.0, 
                         -0.065, -0.038, 0.0, 
                         0.0, 0.0, -0.0004 ],
[ 0,0,1.5*a,0.5*a,0.5*a,0.052, 0.014, 0.014, 
                         0.014, -0.007, 0.003, 
                         0.014, 0.003, -0.007 ],
[ 0,0,1.0*a,1.0*a,1.0*a,0.017, 0.033, 0.033, 
                      0.033, 0.017, 0.033, 
                      0.033, 0.033, 0.017 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
