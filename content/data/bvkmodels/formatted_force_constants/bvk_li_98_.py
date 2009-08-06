#!/usr/bin/python
import System
    
# a scales lattice vectors
a=2.0
m=1.15260710727e-26   # mass in kg of one atom
    
lattice_type = 'bcc'
temperature = 98
reference = 'Smith, H.G., Dolling, G., Nicklow, R.M., Vijayaraghavan, P.R.V., Wilkinson, M.K.: Neutron Inelastic Scattering, IAEA, Vienna Vol. 1, 1968, 149'

cell=[
  a,0,0,
  0,a,0,
  0.5*a,0.5*a,0.5*a,
]

atoms=[
  [ "Li", m ],
]

sites=[
  [ 0*a,0*a,0*a,             0 ],
]

bonds=[
[ 0,0,0.5*a,0.5*a,0.5*a,2.336, 2.462, 2.462, 
                         2.462, 2.336, 2.462, 
                         2.462, 2.462, 2.336 ],
[ 0,0,1.0*a,0.0*a,0.0*a,0.694, 0.0, 0.0, 
                         0.0, 0.14, 0.0, 
                         0.0, 0.0, 0.14 ],
[ 0,0,1.0*a,1.0*a,0.0*a,-0.277, -0.158, 0.0, 
                         -0.158, -0.277, 0.0, 
                         0.0, 0.0, 0.125 ],
[ 0,0,1.5*a,0.5*a,0.5*a,0.171, 0.011, 0.011, 
                         0.011, -0.126, -0.122, 
                         0.011, -0.122, -0.126 ],
[ 0,0,1.0*a,1.0*a,1.0*a,0.148, -0.038, -0.038, 
                      -0.038, 0.148, -0.038, 
                      -0.038, -0.038, 0.148 ],
[ 0,0,2.0*a,0.0*a,0.0*a,-0.282, 0.0, 0.0, 
                      0.0, 0.012, 0.0, 
                      0.0, 0.0, 0.012 ],
]
        
System.write(cell,atoms,sites,bonds,"cubic")
