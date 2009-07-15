# bvk_cu_973.py
# BvK force constants

element = "Cu"
lattice_type = "fcc"
temperature = 973    # Units: K
reference = "Larose, A., Brokchouse, B.N.: Can. J. Phys. 54 (1976) 1990"
details = "General force for next neighbour, otherwise axially symmetric model"

# Units: N m^-1 
force_constants = { "110": { "xx": 11.682, 
                             "zz": -1.424,
                             "xy": 14.384 }, 
                    "200": { "xx": 1.554,
                             "yy": 0.074 },
                    "211": { "xx": 0.658,
                             "yy": 0.193,
                             "yz": 0.155,
                             "xz": 0.310 },
                    "220": { "xx": -0.490,
                             "zz": -0.024,
                             "xy": -0.466 },
                    "310": { "xx": -0.120,
                             "yy": -0.063,
                             "zz": -0.055,
                             "xy": -0.022 } }
