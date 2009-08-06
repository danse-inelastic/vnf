# bvk_ni_298.py
# BvK force constants

element = "Ni"
lattice_type = "fcc"
temperature = 298    # Units: K
reference = "De Wit, G.A., Brockhouse, B.N.: J. Appl. Phys. 39 (1968) 451"
details = "All fits use the measured elastic constants. This fit uses general force up to fourth neighbour, axially symmetric force for fifth neighbour."
a = 3.52   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 17.319, 
                             "zz": -0.436,
                             "xy": 19.100 }, 
                    "200": { "xx": 1.044,
                             "yy": -0.780 },
                    "211": { "xx": 0.842,
                             "yy": 0.263,
                             "yz": -0.109,
                             "xz": 0.424 },
                    "220": { "xx": 0.402,
                             "zz": -0.185,
                             "xy": 0.660 },
                    "310": { "xx": -0.085,
                             "yy": 0.007,
                             "zz": 0.018,
                             "xy": -0.035 } }
