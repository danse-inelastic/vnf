# bvk_cu_673.py
# BvK force constants

element = "Cu"
lattice_type = "fcc"
temperature = 673    # Units: K
reference = "Larose, A., Brokchouse, B.N.: Can. J. Phys. 54 (1976) 1990"
details = "General force for next neighbour, otherwise axially symmetric model"

# Units: N m^-1 
force_constants = { "110": { "xx": 12.275, 
                             "zz": -1.321,
                             "xy": 14.062 }, 
                    "200": { "xx": 0.696,
                             "yy": -0.355 },
                    "211": { "xx": 0.744,
                             "yy": -0.246,
                             "yz": 0.185,
                             "xz": 0.331 },
                    "220": { "xx": -0.174,
                             "zz": -0.024,
                             "xy": -0.150 },
                    "310": { "xx": -0.190,
                             "yy": -0.080,
                             "zz": -0.067,
                             "xy": -0.041 } }
