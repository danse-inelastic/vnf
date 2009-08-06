# bvk_ag_296.py
# BvK force constants

element = "Ag"
lattice_type = "fcc"
temperature = 296    # Units: K
reference = "Kamitakahara, W.A., Brockhouse, B.N.: Phys. Lett. 29A (1969) 639"
a = 4.08   # lattice parameter in angstroms

# Units: N m^-1 
force_constants = {"110": {"xx": 10.71, 
                           "zz": 1.75,
                           "xy": 12.32}, 
                   "200": {"xx": 0.06,
                           "yy": -0.23},
                   "211": {"xx": 0.52,
                           "yy": 0.21,
                           "yz": 0.05,
                           "xz": 0.30},
                   "220": {"xx": -0.13,
                           "xy": -0.14,
                           "zz": 0.01} }
