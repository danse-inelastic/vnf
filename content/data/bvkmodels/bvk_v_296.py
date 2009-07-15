# bvk_v_296.py
# BvK force constants

element = "V"
lattice_type = "bcc"
temperature = 296    # Units: K
reference = "Cohen, M., Heine, V., Weaire, D.: Solid State Phys. (H. Ehrenreich, F. Seitz and D. Turnbull eds.) Academic Press, New York 24 (1970)"
details = "Model B. Calculated from fitted interplanar force constants. Generally poorer fitting than model A (direct fit to the phonon dispersion), but better agreement with the measured spectrum."

# Units: N m^-1 
force_constants = { "111": { "xx": 10.534, 
                             "xy": 6.305 }, 
                    "200": { "xx": 7.129,
                             "yy": -0.955 },
                    "220": { "xx": 2.730,
                             "zz": -4.494,
                             "xy": 0.952 },
                    "311": { "xx": 1.555,
                             "yy": 0.420,
                             "yz": -1.527,
                             "xz": 0.977 },
                    "222": { "xx": -0.296,
                             "xy": 0.263 },
                    "400": { "xx": -1.389,
                             "yy": 0.660 },
                    "133": { "xx": -0.094,
                             "yy": -0.653,
                             "yz": -0.822,
                             "xy": 0.397 } }
