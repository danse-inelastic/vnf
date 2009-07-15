# bvk_rb_12.py
# BvK force constants

element = "Rb"
lattice_type = "bcc"
temperature = 12    # Units: K
reference = "Copley, J.R.D., Brockhouse, B.N.: Can. J. Phys. 51 (1973) 657"
details = "The dispersion curves can be fitted with a fourth neighbour model. Increasing the number of parameters changes the fit only marginally."

# Units: N m^-1 
force_constants = { "111": { "xx": 0.669, 
                             "xy": 0.788 }, 
                    "200": { "xx": 0.397,
                             "yy": 0.022 },
                    "220": { "xx": -0.037,
                             "zz": -0.009,
                             "xy": 0.043 },
                    "311": { "xx": 0.018,
                             "yy": -0.004,
                             "yz": -0.010,
                             "xz": -0.009 } }
