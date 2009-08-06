# bvk_nb_296.py
# BvK force constants

element = "Nb"
lattice_type = "bcc"
temperature = 296    # Units: K
reference = "Nakagawa, Y., Wooods, A.D.B.: Phys. Rev. Lett. 11 (1963) 271"
a = 3.29   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "111": { "xx": 14.14, 
                             "xy": 8.84 }, 
                    "200": { "xx": 14.16,
                             "yy": -3.64 },
                    "220": { "xx": 2.27,
                             "zz": -6.38,
                             "xy": 0.79 },
                    "311": { "xx": 3.61,
                             "yy": -0.75,
                             "yz": -0.95,
                             "xz": 1.26 },
                    "222": { "xx": -1.16,
                             "xy": -1.33 },
                    "400": { "xx": -7.08,
                             "yy": 1.32 },
                    "133": { "xx": -0.03,
                             "yy": -0.10,
                             "yz": 0.37,
                             "xy": -0.17 },
                    "420": { "xx": 0.51,
                             "yy": -0.27,
                             "zz": 0.81,
                             "xy": -0.06 } }
