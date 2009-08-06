# bvk_pd_673.py
# BvK force constants

element = "Pd"
lattice_type = "fcc"
temperature = 673    # Units: K
reference = "Miiller, A.P., Brockhouse, B.N.: Can. J. Phys. 49 (1971) 704"
a = 3.88   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 17.599, 
                             "zz": -2.412,
                             "xy": 21.350 }, 
                    "200": { "xx": 1.390,
                             "yy": 0.044 },
                    "211": { "xx": 0.661,
                             "yy": 0.388,
                             "yz": 0.039,
                             "xz": 0.784 },
                    "220": { "xx": -0.720,
                             "zz": -0.177,
                             "xy": -1.283 },
                    "310": { "xx": 0.217,
                             "yy": -0.228,
                             "zz": -0.284,
                             "xy": 0.167 },
                    "222": { "xx": -0.063,
                             "xy": 0.116 },
                    "321": { "xx": -0.139,
                             "yy": 0.155,
                             "zz": 0.012,
                             "yz": -0.030,
                             "xz": -0.045,
                             "xy": -0.090 },
                    "400": { "xx": 0.071,
                             "yy": 0.028 } }
