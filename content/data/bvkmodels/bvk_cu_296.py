# bvk_cu_296.py
# BvK force constants

element = "Cu"
lattice_type = "fcc"
temperature = 296    # Units: K
reference = "Svensson, E.C., Brockhouse, B.N., Rowe, J.M.: Phys. Rev. 155 (1967) 619"
details = "Axially symmetric 5th neighbor force constants"

# Units: N m^-1 
force_constants = { "110": { "xx": 13.102, 
                             "zz": -1.417,
                             "xy": 14.820 }, 
                    "200": { "xx": 0.361,
                             "yy": -0.238 },
                    "211": { "xx": 0.642,
                             "yy": 0.315,
                             "yz": 0.190,
                             "xz": 0.385 },
                    "220": { "xx": 0.104,
                             "zz": -0.284,
                             "xy": 0.396 },
                    "310": { "xx": -0.137,
                             "yy": 0.009,
                             "zz": -0.016,
                             "xy": -0.055 },
                    "222": { "xx": -0.138,
                             "yz": -0.232 } }
