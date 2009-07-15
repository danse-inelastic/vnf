# bvk_k_9_a.py
# BvK force constants

element = "K"
lattice_type = "bcc"
temperature = 9    # Units: K
reference = "Dolling, G., Meyer, J.: J. Phys. F7 (1977) 775"
details = "Axially symmetric model"

# Units: N m^-1 
force_constants = { "111": { "xx": 0.7688, 
                             "xy": 0.8805 }, 
                    "200": { "xx": 0.4042,
                             "yy": 0.0296 },
                    "220": { "xx": -0.0418,
                             "zz": 0.0038,
                             "xy": -0.0455 },
                    "311": { "xx": 0.0213,
                             "yy": -0.0029,
                             "yz": 0.0030,
                             "xz": 0.0091 },
                    "222": { "xx": 0.0091,
                             "xy": 0.0062 } }
