# bvk_cu_80.py
# BvK force constants

element = "Cu"
lattice_type = "fcc"
temperature = 80    # Units: K
reference = "Nilsson, G., Rolandson, S.: Phys. Rev. B7 (1973) 2393"
details = "General forces determined largely from off symmetry phonons"

# Units: N m^-1 
force_constants = { "110": { "xx": 13.570, 
                             "zz": -1.078,
                             "xy": 15.542 }, 
                    "200": { "xx": 0.199,
                             "yy": -0.209 },
                    "211": { "xx": 0.442,
                             "yy": 0.315,
                             "yz": 0.113,
                             "xz": 0.217 },
                    "220": { "xx": 0.112,
                             "zz": -0.100,
                             "xy": 0.226 },
                    "310": { "xx": -0.223,
                             "yy": -0.020,
                             "zz": -0.186,
                             "xy": 0.084 },
                    "222": { "xx": -0.141,
                             "yz": -0.126 },
                    "321": { "xx": 0.022,
                             "yy": 0.100,
                             "zz": -0.031,
                             "yz": -0.006,
                             "xz": -0.040,
                             "xy": 0.034 },
                    "400": { "xx": 0.016,
                             "yy": 0.123} }
