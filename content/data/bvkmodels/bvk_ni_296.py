# bvk_ni_296.py
# BvK force constants

element = "Ni"
lattice_type = "fcc"
temperature = 296    # Units: K
reference = "Birgenau, R.J., Cordes, J. Dolling, G., Woods, A.D.B.: Phys. Rev. 136 (1964) A 1359"
details = "All fits use the measured elastic constants. This fit uses axially symmetric forces."
a = 3.52   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 17.720, 
                             "zz": -1.015,
                             "xy": 18.735 }, 
                    "200": { "xx": 1.148,
                             "yy": -0.998 },
                    "211": { "xx": 0.940,
                             "yy": 0.182,
                             "yz": 0.505,
                             "xz": 0.253 },
                    "220": { "xx": 0.459,
                             "zz": -0.153,
                             "xy": 0.612 },
                    "310": { "xx": -0.363,
                             "yy": 0.100,
                             "zz": 0.158,
                             "xy": -0.174 } }
