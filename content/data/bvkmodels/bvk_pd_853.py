# bvk_pd_853.py
# BvK force constants

element = "Pd"
lattice_type = "fcc"
temperature = 853    # Units: K
reference = "Miiller, A.P., Brockhouse, B.N.: Can. J. Phys. 49 (1971) 704"
a = 3.88   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 17.383, 
                             "zz": -2.877,
                             "xy": 20.766 }, 
                    "200": { "xx": 2.001,
                             "yy": 0.098 },
                    "211": { "xx": 0.875,
                             "yy": 0.116,
                             "yz": 0.373,
                             "xz": 0.339 },
                    "220": { "xx": -0.546,
                             "zz": 0.078,
                             "xy": -0.026 },
                    "310": { "xx": -0.263,
                             "yy": -0.148,
                             "zz": -0.134,
                             "xy": -0.043 },
                    "222": { "xx": -0.233,
                             "xy": -0.015 },
                    "321": { "xx": -0.057,
                             "yy": 0.032,
                             "zz": 0.051,
                             "yz": -0.021,
                             "xz": -0.032,
                             "xy": -0.063 },
                    "400": { "xx": 0.223,
                             "yy": 0.002 } }
