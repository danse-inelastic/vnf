# bvk_pt_90.py
# BvK force constants

element = "Pt"
lattice_type = "fcc"
temperature = 90    # Units: K
reference = "Dutton, D.H., Brockhouse, B.N., Miiller, A.P.: Can. J. Phys. 50 (1972) 2915"
details = "The force constants to the fifth neighbours are axially symmetric. A fit to the experimental data requires force constants to the fourth neighbours. Weaker forces probably extend to at least the sixth neighbours. Extending the fit to eighth neighbours improves the goodness of the fit only marginally."

# Units: N m^-1 
force_constants = { "110": { "xx": 25.834, 
                             "zz": -6.918,
                             "xy": 29.787 }, 
                    "200": { "xx": 3.935,
                             "yy": -0.916 },
                    "211": { "xx": 1.732,
                             "yy": 0.237,
                             "yz": 0.819,
                             "xz": 1.335 },
                    "220": { "xx": -2.490,
                             "zz": -0.467,
                             "xy": -2.331 },
                    "310": { "xx": 0.640,
                             "yy": 0.021,
                             "zz": -0.056,
                             "xy": 0.233 },
                    "222": { "xx": 0.468,
                             "yz": -0.263 } }
