# bvk_cu_49.py
# BvK force constants

element = "Cu"
lattice_type = "fcc"
temperature = 49    # Units: K
reference = "Nicklow, R.M., Gilat, G., Smith, H.G., Raubenheimer, L.J., Wilkinson, M.K.: Phys. Rev. 164 (1967) 922"
details = "Axially symmetric model, fit includes isothermal elastic constants"
a = 3.61   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 13.278, 
                             "zz": -1.351,
                             "xy": 14.629 }, 
                    "200": { "xx": -0.041,
                             "yy": -0.198 },
                    "211": { "xx": 0.742,
                             "yy": 0.284,
                             "yz": 0.153,
                             "xz": 0.306 },
                    "220": { "xx": 0.350,
                             "zz": -0.327,
                             "xy": 0.677 },
                    "310": { "xx": -0.195,
                             "yy": -0.006,
                             "zz": 0.017,
                             "xy": -0.071 },
                    "222": { "xx": -0.137,
                             "xy": -0.135 } }

