# bvk_al_300.py
# BvK force constants

element = "Al"
lattice_type = "fcc"
temperature = 300    # Units: K
reference = "Gilat, G., Nicklow, R.M.: Phys. Rev. 143 (1965) 487"
details = "Axially symmetric fit to elastic constants and phonons in symmetry directions"
a = 4.04   # lattice parameter in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 9.808, 
                             "zz": -1.616,
                             "xy": 11.424 }, 
                    "200": { "xx": 2.494,
                             "yy": -0.515 },
                    "211": { "xx": -0.439,
                             "yy": -0.167,
                             "yz": -0.091,
                             "xz": -0.182 },
                    "220": { "xx": 0.027,
                             "zz": 0.465,
                             "xy": -0.438 },
                    "310": { "xx": 0.518,
                             "yy": 0.141,
                             "zz": 0.094,
                             "xy": 0.141 },
                    "222": { "xx": 0.076,
                             "xy": -0.061 },
                    "321": { "xx": -0.049,
                             "yy": -0.065,
                             "zz": -0.074,
                             "yz": 0.006,
                             "xz": 0.009,
                             "xy": 0.019 },
                    "400": { "xx": -0.756,
                             "yy": -0.063 } }
