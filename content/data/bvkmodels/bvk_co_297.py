# bvk_co_297.py
# BvK force constants

element = "Co"
lattice_type = "fcc"
temperature = 297    # Units: K
reference = "Svensson, E.C., Powell, B.M., Woods, A.D.B., Teuchert, W-D.: Can J. Phys. 57 (1979) 253"
details = "Co_0.92Fe_0.08"

# Units: N m^-1 
force_constants = { "110": { "xx": 15.71, 
                             "zz": 0.27,
                             "xy": 18.77 }, 
                    "200": { "xx": 0.32,
                             "yy": 0.27 },
                    "211": { "xx": 0.36,
                             "yy": -0.20,
                             "yz": 0.38,
                             "xz": 0.27 },
                    "220": { "xx": 1.52,
                             "zz": 0.09,
                             "xy": 1.36 } }
