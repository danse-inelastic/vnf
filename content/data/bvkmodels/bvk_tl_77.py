# bvk_tl_77.py
# BvK force constants

element = "Tl"
lattice_type = "hcp"
temperature = 77    # Units: K
reference = "Worlton, T.G., Schmunk, R.E.: Phys. Rev. B3 (1971) 4115"
details = "The model is of the 'modified axially symmetric' form."

# Units: N m^-1 
force_constants = { "1" : { "K" : 10.2475,
                            "C_Bx" : -1.9278,
                            "C_Bz" : 3.6872 },
                    "2" : { "K" : 10.5406,
                            "C_Bx" : -0.0733,
                            "C_Bz" : 0.1402 },
                    "3" : { "K" : -2.386,
                            "C_Bx" : 0.8603,
                            "C_Bz" : -1.6455 },
                    "4" : { "K" : -1.4887,
                            "C_Bx" : -0.2527,
                            "C_Bz" : 0.4833 },
                    "5" : { "K" : 1.8162,
                            "C_Bx" : 0.0314,
                            "C_Bz" : -0.0601 },
                    "6" : { "K" : -1.1599,
                            "C_Bx" : 0.1008,
                            "C_Bz" : -0.1930 } }

