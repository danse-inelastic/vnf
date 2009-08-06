# bvk_zr_295.py
# BvK force constants

element = "Zr"
lattice_type = "hcp"
temperature = 295   # Units: K
reference = "Stassis, C., Zarestky, J., Arch, D., McMasters, O.D., Harmon, B.N.: Phys. Rev. B18 (1978) 2632"
a = 3.23   # lattice parameters in angstroms, for alpha Zr
c = 5.14

# For beta Zr:
# a = 3.61

# Units: N m^-1 
force_constants = { "1" : { "K" : 39.74,
                            "C_Bx" : -3.77,
                            "C_Bz" : -12.88 },
                    "2" : { "K" : 22.80,
                            "C_Bx" : -0.70,
                            "C_Bz" : 3.28 },
                    "3" : { "K" : -4.60,
                            "C_Bx" : -0.39,
                            "C_Bz" : -1.45 },
                    "4" : { "K + C_Bz" : 8.40,
                            "C_Bx" : 0.43 },
                    "5" : { "K" : 1.95,
                            "C_Bx" : 0.28,
                            "C_Bz" : -0.26 },
                    "6" : { "K" : 1.48,
                            "C_Bx" : 1.71,
                            "C_Bz" : 0.10 } } 

