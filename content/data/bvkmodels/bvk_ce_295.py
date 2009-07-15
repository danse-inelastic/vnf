# bvk_ce_295.py
# BvK force constants

element = "Ce"
lattice_type = "fcc" # gamma-phase
temperature = 80    # Units: K
reference = "Stassis, C., Gould, T., McMasters, O.D., Gschneider, K.A., Nicklow, R.M.: Phys. Rev B19 (1979) 5746"
details = "Axially symmetric fit to elastic constants and phonons in symmetry directions"

# Units: N m^-1 
force_constants = { "110": { "xx": 4.3726, 
                             "zz": -0.2264,
                             "xy": 4.5798}, 
                    "200": { "xx": -2.3562,
                             "yy": 0.0773 },
                    "211": { "xx": 0.2058,
                             "yy": 0.3169,
                             "yz": -0.0547,
                             "xz": -0.0496 },
                    "220": { "xx": 0.1231,
                             "zz": 0.0114,
                             "xy": 0.1505 },
                    "310": { "xx": -0.0525,
                             "yy": -0.0992,
                             "zz": -0.1044,
                             "xy": 0.0193 },
                    "222": { "xx": -0.3316,
                             "xy": -0.2194 },
                    "321": { "xx": 0.1057,
                             "yy": -0.1138,
                             "zz": 0.0263,
                             "yz": 0.0050,
                             "xz": 0.0763,
                             "xy": -0.0068 },
                    "400": { "xx": -0.0009,
                             "yy": 0.2219 } }
