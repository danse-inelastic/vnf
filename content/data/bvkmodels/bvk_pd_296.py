# bvk_pd_296.py
# BvK force constants

element = "Pd"
lattice_type = "fcc"
temperature = 296    # Units: K
reference = "Miiller, A.P., Brockhouse, B.N.: Can. J. Phys. 49 (1971) 704"
a = 3.88   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 19.337, 
                             "zz": -2.832,
                             "xy": 22.423 }, 
                    "200": { "xx": 1.424,
                             "yy": 0.210 },
                    "211": { "xx": 0.744,
                             "yy": 0.249,
                             "yz": 0.163,
                             "xz": 0.708 },
                    "220": { "xx": -1.142,
                             "zz": -0.223,
                             "xy": -1.370 },
                    "310": { "xx": -0.006,
                             "yy": -0.207,
                             "zz": -0.232,
                             "xy": 0.076 },
                    "222": { "xx": 0.154,
                             "xy": 0.330 },
                    "321": { "xx": 0.070,
                             "yy": 0.067,
                             "zz": -0.020,
                             "yz": -0.022,
                             "xz": -0.032,
                             "xy": -0.065 },
                    "400": { "xx": 0.072,
                             "yy": 0.006 } }
