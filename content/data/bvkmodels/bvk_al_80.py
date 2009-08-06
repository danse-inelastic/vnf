# bvk_al_80.py
# BvK force constants

element = "Al"
lattice_type = "fcc"
temperature = 80    # Units: K
reference = "Cowley, E.R.: Can. J. Phys. 52 (1974) 1714"
details = "Fit to elastic constants and phonons including off symmetry directions"
a = 4.04   # lattice parameter in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 10.4578, 
                             "zz": -2.6322,
                             "xy": 10.3657 }, 
                    "200": { "xx": 2.4314,
                             "yy": -0.1351 },
                    "211": { "xx": 0.0986,
                             "yy": -0.2366,
                             "yz": -0.2862,
                             "xz": -0.1819 },
                    "220": { "xx": 0.1363,
                             "zz": 0.1854,
                             "xy": 0.3753 },
                    "310": { "xx": -0.3003,
                             "yy": 0.1842,
                             "zz": 0.2603,
                             "xy": -0.3239 },
                    "222": { "xx": -0.1412,
                             "xy": 0.1990 },
                    "321": { "xx": 0.1828,
                             "yy": -0.2207,
                             "zz": -0.0173,
                             "yz": -0.0214,
                             "xz": -0.0747,
                             "xy": 0.0397 },
                    "400": { "xx": -0.0681,
                             "yy": -0.0202 } }
