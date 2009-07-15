# bvk_cu_1336.py
# BvK force constants

element = "Cu"
lattice_type = "fcc"
temperature = 1336    # Units: K
reference = "Larose, A., Brokchouse, B.N.: Can. J. Phys. 54 (1976) 1990"
details = "General force for next neighbour, otherwise axially symmetric model"

# Units: N m^-1 
force_constants = { "110": { "xx": 11.718, 
                             "zz": -1.787,
                             "xy": 13.653 }, 
                    "200": { "xx": 0.238,
                             "yy": -0.279 },
                    "211": { "xx": 0.325,
                             "yy": 0.095,
                             "yz": 0.076,
                             "xz": 0.153 },
                    "220": { "xx": -0.246,
                             "zz": 0.093,
                             "xy": -0.339 },
                    "310": { "xx": -0.074,
                             "yy": -0.092,
                             "zz": -0.095,
                             "xy": 0.007 } }
