# bvk_rb_120.py
# BvK force constants

element = "Rb"
lattice_type = "bcc"
temperature = 120    # Units: K
reference = "Copley, J.R.D., Brockhouse, B.N.: Can. J. Phys. 51 (1973) 657"
details = "The dispersion curves can be fitted with a fourth neighbour model. Increasing the number of parameters changes the fit only marginally."

# Units: N m^-1 
force_constants = { "111": { "xx": 0.618, 
                             "xy": 0.740 }, 
                    "200": { "xx": 0.456,
                             "yy": 0.012 },
                    "220": { "xx": -0.034,
                             "zz": -0.003,
                             "xy": -0.061 },
                    "311": { "xx": -0.003,
                             "yy": 0.000,
                             "yz": 0.004,
                             "xz": 0.003 } }
