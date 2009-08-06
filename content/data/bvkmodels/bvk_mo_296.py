# bvk_mo_296.py
# BvK force constants

element = "Mo"
lattice_type = "bcc"
temperature = 296    # Units: K
reference = "Walker, C.B., Egelstaff, P.A.: Phys. Rev. 177 (1969)"
details = "The gross features of the dispersion can be described by a third neighbour model. A detailed description necessitates long range forces."
a = 3.14   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "111": { "xx": 15.82, 
                             "xy": 12.00 }, 
                    "200": { "xx": 42.22,
                             "yy": -1.54},
                    "220": { "xx": 2.44,
                             "zz": -0.57,
                             "xy": 1.92 },
                    "311": { "xx": -1.55,
                             "yy": 0.14,
                             "yz": 0.76,
                             "xz": 0.58 },
                    "222": { "xx": 0.74,
                             "xy": 0.36 },
                    "400": { "xx": 4.54,
                             "yy": -0.51 },
                    "133": { "xx": -0.84,
                             "yy": 0.59,
                             "yz": -0.16,
                             "xz": 0.11 } }
