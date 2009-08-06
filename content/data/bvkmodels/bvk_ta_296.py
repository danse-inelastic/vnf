# bvk_ta_296.py
# BvK force constants

element = "Ta"
lattice_type = "bcc"
temperature = 296    # Units: K
reference = "Woods, A.D.B., Chen, S.H.: Solid State Commun. 2 (1964) 233"
details = "General force model"
a = 3.60   # lattice parameters in angstroms
c = 5.70

# Units: N m^-1 
force_constants = { "111": { "xx": 16.983, 
                             "xy": 11.201 }, 
                    "200": { "xx": 1.182,
                             "yy": 1.423 },
                    "220": { "xx": 3.546,
                             "zz": -5.427,
                             "xy": 1.943 },
                    "311": { "xx": 3.577,
                             "yy": -0.718,
                             "yz": -1.728,
                             "xz": 0.983 },
                    "222": { "xx": -0.493,
                             "xy": 0.812 },
                    "400": { "xx": -3.705,
                             "yy": -0.237,
                             "yz": 0.106,
                             "xy": -0.683 } }
