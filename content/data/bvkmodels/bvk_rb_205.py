# bvk_rb_205.py
# BvK force constants

element = "Rb"
lattice_type = "bcc"
temperature = 205    # Units: K
reference = "Copley, J.R.D., Brockhouse, B.N.: Can. J. Phys. 51 (1973) 657"
details = "The dispersion curves can be fitted with a fourth neighbour model. Increasing the number of parameters changes the fit only marginally."

# Units: N m^-1 
force_constants = { "111": { "xx": 0.591, 
                             "xy": 0.680 }, 
                    "200": { "xx": 0.438,
                             "yy": -0.035 },
                    "220": { "xx": -0.014,
                             "zz": 0.010,
                             "xy": -0.075 },
                    "311": { "xx": -0.016,
                             "yy": -0.011,
                             "yz": 0.000,
                             "xz": 0.007 } }
