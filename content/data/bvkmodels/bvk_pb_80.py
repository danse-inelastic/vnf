# bvk_pb_80.py
# BvK force constants

element = "Pb"
lattice_type = "fcc"
temperature = 80    # Units: K
reference = "Cowley, E.R.: Solid State Commun. 14 (1974) 587"
details = "The interionic forces in Pb are very long range and BvK fits are therefore only of limited value. The spectrum calculated from an eighth neighbour fit to the symmetry phonons differs considerably from the one obtained directly by interpolation of the measured phonon frequencies. Utilizing the off symmetry phonon frequencies to fit the force constants of the spectrum can be fairly well reproduced."

# Units: N m^-1 
force_constants = { "110": { "xx": 4.3243, 
                             "zz": -2.4881,
                             "xy": 4.6730 }, 
                    "200": { "xx": 1.4083,
                             "yy": 0.0719 },
                    "211": { "xx": 0.2764,
                             "yy": -2.996,
                             "yz": -0.0434,
                             "xz": 0.0722 },
                    "220": { "xx": 0.7414,
                             "zz": 0.2446,
                             "xy": 0.4117 },
                    "310": { "xx": -0.5136,
                             "yy": -0.1424,
                             "zz": 0.3011,
                             "xy": -0.1920 },
                    "321": { "xx": 0.2604,
                             "yy": -0.2002,
                             "zz": 0.0078,
                             "yz": -0.0082,
                             "xz": -0.1973,
                             "xy": 0.0805 },
                    "400": { "xx": -0.0881,
                             "yy": -0.0900 } }
