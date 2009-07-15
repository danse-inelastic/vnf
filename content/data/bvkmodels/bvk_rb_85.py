# bvk_rb_85.py
# BvK force constants

element = "Rb"
lattice_type = "bcc"
temperature = 85    # Units: K
reference = "Copley, J.R.D., Brockhouse, B.N.: Can. J. Phys. 51 (1973) 657"
details = "The dispersion curves can be fitted with a fourth neighbour model. Increasing the number of parameters changes the fit only marginally."

# Units: N m^-1 
force_constants = { "111": { "xx": 0.657, 
                             "xy": 0.746 }, 
                    "200": { "xx": 0.400,
                             "yy": 0.007 },
                    "220": { "xx": -0.013,
                             "zz": -0.025,
                             "xy": -0.011 },
                    "311": { "xx": -0.013,
                             "yy": -0.003,
                             "yz": -0.027,
                             "xz": -0.002 } }
