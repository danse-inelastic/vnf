# bvk_w_298.py
# BvK force constants

element = "W"
lattice_type = "bcc"
temperature = 298    # Units: K
reference = "Larose, A., Brockhouse, B.N.: Can. J. Phys. 54 (1976) 1819"
details = "Fit to the data of Chen, S.H.: Thesis, Mc. Master University, Hamilton, Ontario, Canada 1964 and Larose (see reference)"

# Units: N m^-1 
force_constants = { "111": { "xx": 22.1, 
                             "xy": 18.9 }, 
                    "200": { "xx": 45.7,
                             "yy": 0.7 },
                    "220": { "xx": 3.7,
                             "zz": -1.3,
                             "xy": 5.2 } }
