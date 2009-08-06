# bvk_ti_295.py
# BvK force constants

element = "Ti"
lattice_type = "hcp"
temperature = 295    # Units: K
reference = "Stassis, C., Arch, D., Harmon, B.N., Wakabayashi, N.: Phys. Rev. B19 (1979) 181"
details = "The model is of the 'modified axially symmetric' form."
a = 2.95   # lattice parameters in angstroms
c = 4.68

# Units: N m^-1 
force_constants = { "1" : { "K" : 41.38,
                            "C_Bx" : -3.03,
                            "C_Bz" : -17.21 },
                    "2" : { "K" : 22.28,
                            "C_Bx" : 0.171,
                            "C_Bz" : 3.78 },
                    "3" : { "K" : -8.33,
                            "C_Bx" : 1.10,
                            "C_Bz" : 0.22 },
                    "4" : { "K + C_Bz" : 12.20,
                            "C_Bx" : 0.68 },
                    "5" : { "K" : 2.26,
                            "C_Bx" : 0.17,
                            "C_Bz" : 0.02 },
                    "6" : { "K" : 0.65,
                            "C_Bx" : 1.51,
                            "C_Bz" : 0.23 } }

