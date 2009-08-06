# bvk_tl_296.py
# BvK force constants

element = "Tl"
lattice_type = "hcp"
temperature = 296    # Units: K
reference = "Worlton, T.G., Schmunk, R.E.: Phys. Rev. B3 (1971) 4115"
details = "The model is of the 'modified axially symmetric' form."
a = 3.45   # lattice parameters in angstroms
c = 5.51

# Units: N m^-1 
force_constants = { "1" : { "K" : 15.4911,
                            "C_Bx" : -2.4216,
                            "C_Bz" : -3.7824 },
                    "2" : { "K" : 12.8704,
                            "C_Bx" : -1.1571,
                            "C_Bz" : -1.8073 },
                    "3" : { "K" : -0.4819,
                            "C_Bx" : 0.6088,
                            "C_Bz" : -0.9509 },
                  #  "4" : { "K" : -0.8846,
                  #          "C_Bx" : 0.0785,
                  #          "C_Bz" : 0.1226 },
                    "4" : { "K + C_Bz" : -0.8846 + 0.1226,
                            "C_Bx" : 0.0785 },
                    "5" : { "K" : -0.2955,
                            "C_Bx" : 0.1774,
                            "C_Bz" : 0.2771 },
                    "6" : { "K" : -0.3212,
                            "C_Bx" : -0.2748,
                            "C_Bz" : -0.4292 } }

