# bvk_li_293.py
# BvK force constants

element = "Li"
lattice_type = "bcc"
temperature = 293    # Units: K
reference = "Beg, M.M., Nielsen, M.: Phys. Rev. B14 (1976) 4266"
a = 3.50   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "111": { "xx": 2.114, 
                             "xy": 2.207 }, 
                    "200": { "xx": 0.862,
                             "yy": 0.016 },
                    "220": { "xx": -0.268,
                             "zz": 0.055,
                             "xy": -0.197 },
                    "311": { "xx": 0.146,
                             "yy": -0.057,
                             "yz": 0.033,
                             "xz": 0.052 },
                    "222": { "xx": 0.062,
                             "xy": 0.077 } }
