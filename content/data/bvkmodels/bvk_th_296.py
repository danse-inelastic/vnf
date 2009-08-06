# bvk_th_296.py
# BvK force constants

element = "Th"
lattice_type = "fcc"
temperature = 296    # Units: K
reference = "Reese, R.A., Sinha, S.K., Peterson, D.T.: Phys. Rev. B8 (1973) 1332"
details = "The force constants are constrained to fit the elastic constants. Axial symmetry conditions are imposed on the fifth and seventh neighbour constants."
a = 5.08   # lattice parameters in angstroms

# Units: N m^-1 
force_constants = { "110": { "xx": 1.181, 
                             "zz": -0.218,
                             "xy": 1.176 }, 
                    "200": { "xx": -0.090,
                             "yy": -0.093 },
                    "211": { "xx": -0.035,
                             "yy": 0.015,
                             "yz": 0.060,
                             "xz": -0.072 },
                    "220": { "xx": -0.013,
                             "zz": 0.096,
                             "xy": 0.054 },
                    "310": { "xx": -0.041,
                             "yy": -0.008,
                             "zz": -0.003,
                             "xy": -0.013 },
                    "222": { "xx": -0.034,
                             "xy": -0.061 },
                    "321": { "xx": 0.013,
                             "yy": 0.043,
                             "zz": -0.021,
                             "yz": 0.009,
                             "xz": 0.013,
                             "xy": 0.026 } }
