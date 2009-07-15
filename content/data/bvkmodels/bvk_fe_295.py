# bvk_fe_295.py
# BvK force constants

element = "Fe"
lattice_type = "bcc"  # Alpha phase
temperature = 295    # Units: K
reference = "Minkiewicz, V.J., Shirane, G., Nathans, R.: Phys. Rev. 162 (1967) 528"

# Units: N m^-1 
force_constants = { "111": { "xx": 16.88, 
                             "xy": 15.01 }, 
                    "200": { "xx": 14.63,
                             "yy": 0.55 },
                    "220": { "xx": 0.92,
                             "zz": -0.57,
                             "xy": 0.69 },
                    "311": { "xx": -0.12,
                             "yy": 0.03,
                             "yz": 0.52,
                             "xz": 0.007 },
                    "222": { "xx": -0.29,
                             "xy": 0.32 } }
