# bvk_au_295_b.py
# BvK force constants

element = "Au"
lattice_type = "fcc"
temperature = 295    # Units: K
reference = "Gilat, G., Nicklow, R.M.: Phys. Rev. 143 (1965) 487"
details = "M2 general 1st neighbour force constants and axially symmetric 2nd to 5th neighbour force constants"

# Units: N m^-1 
force_constants = { "110": { "xx": 16.61, 
                             "zz": -6.65,
                             "xy": 19.93 }, 
                    "200": { "xx": 3.95,
                             "yy": -1.13 },
                    "211": { "xx": 1.00,
                             "yy": 0.28,
                             "yz": 0.24,
                             "xz": 0.48 },
                    "220": { "xx": -0.57,
                             "zz": -0.21,
                             "xy": -0.36 },
                    "310": { "xx": -0.17,
                             "yy": -0.02,
                             "zz": 0.00,
                             "xy": -0.06 } }
