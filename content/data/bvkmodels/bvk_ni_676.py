# bvk_ni_676.py
# BvK force constants

element = "Ni"
lattice_type = "fcc"
temperature = 676    # Units: K
reference = "De Wit, G.A., Brockhouse, B.N.: J. Appl. Phys. 39 (1968) 451"
details = "All fits use the measured elastic constants. This fit uses general force up to fourth neighbour, axially symmetric force for fifth neighbour."
a = 3.52   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 16.250, 
                             "zz": -0.970,
                             "xy": 19.390 }, 
                    "200": { "xx": 1.070,
                             "yy": 0.056 },
                    "211": { "xx": 0.963,
                             "yy": 0.449,
                             "yz": -0.391,
                             "xz": 0.458 },
                    "220": { "xx": 0.115,
                             "zz": -0.457,
                             "xy": 0.222 },
                    "310": { "xx": -0.256,
                             "yy": -0.063,
                             "zz": -0.040,
                             "xy": -0.072 } }
