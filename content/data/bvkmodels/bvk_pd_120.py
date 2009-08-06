# bvk_pd_120.py
# BvK force constants

element = "Pd"
lattice_type = "fcc"
temperature = 120    # Units: K
reference = "Miller, A.P., Brockhouse, B.N.: Can. J. Phys. 49 (1971) 704"
a = 3.88   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 19.760, 
                             "zz": -2.511,
                             "xy": 23.194 }, 
                    "200": { "xx": 0.919,
                             "yy": 0.416 },
                    "211": { "xx": 0.907,
                             "yy": 0.134,
                             "yz": 0.609,
                             "xz": 0.912 },
                    "220": { "xx": -1.041,
                             "zz": -0.128,
                             "xy": -1.865 },
                    "310": { "xx": 0.086,
                             "yy": -0.227,
                             "zz": -0.266,
                             "xy": 0.118 },
                    "222": { "xx": 0.219,
                             "xy": 0.154 },
                    "321": { "xx": -0.094,
                             "yy": -0.051,
                             "zz": 0.041,
                             "yz": -0.022,
                             "xz": -0.033,
                             "xy": -0.066 },
                    "400": { "xx": 0.528,
                             "yy": -0.113 } }
