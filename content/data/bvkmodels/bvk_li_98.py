# bvk_li_98.py
# BvK force constants

element = "Li"
lattice_type = "bcc"
temperature = 98    # Units: K
reference = "Smith, H.G., Dolling, G., Nicklow, R.M., Vijayaraghavan, P.R.V., Wilkinson, M.K.: Neutron Inelastic Scattering, IAEA, Vienna Vol. 1, 1968, 149"
a = 3.50   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "111": { "xx": 2.336, 
                             "xy": 2.462 }, 
                    "200": { "xx": 0.694,
                             "yy": 0.140 },
                    "220": { "xx": -0.277,
                             "zz": 0.125,
                             "xy": -0.158 },
                    "311": { "xx": 0.171,
                             "yy": -0.126,
                             "yz": -0.122,
                             "xz": 0.011 },
                    "222": { "xx": 0.148,
                             "xy": -0.038 },
                    "400": { "xx": -0.282,
                             "yy": 0.012 } }
