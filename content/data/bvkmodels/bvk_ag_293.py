# bvk_ag_293.py
# BvK force constants

element = "Ag"
lattice_type = "fcc"
temperature = 293    # Units: K
reference = "Drexel, W.: Z. Phys. 255 (1972) 281, Drexel, W.: Rep KFK 1383, Kernforschungsanlage Karlsruhe, Germany 1971"

# Units: N m^-1 
force_constants = { "110": { "xx": 10.4, 
                             "zz": -1.0,
                             "xy": 12.1 }, 
                    "200": { "xx": -1.6,
                             "yy": -0.5 },
                    "211": { "xx": -0.1,
                             "yy": 0.3,
                             "yz": 0.0,
                             "xz": 1.0 },
                    "220": { "xx": 0.3,
                             "yy": -0.3,
                             "zz": 0.2 } }
