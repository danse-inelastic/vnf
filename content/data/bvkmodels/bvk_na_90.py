# bvk_na_90.py
# BvK force constants

element = "Na"
lattice_type = "bcc"
temperature = 90    # Units: K
reference = "Woods, A.D.B., Brockhouse, B.N., March, R.H., Stewart, A.T., Bowers, R.: Phys. Rev. 128 (1962) 1112"

# Units: N m^-1 
force_constants = { "111": { "xx": 1.178, 
                             "xy": 1.1320 }, 
                    "200": { "xx": 0.472,
                             "yy": 0.104 },
                    "220": { "xx": -0.038,
                             "zz": -0.0004,
                             "xy": -0.065 },
                    "311": { "xx": 0.052,
                             "yy": -0.007,
                             "yz": 0.003,
                             "xz": 0.014 },
                    "222": { "xx": 0.017,
                             "xy": 0.033 } }
