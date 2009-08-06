# bvk_zn_80.py
# BvK force constants

element = "Zn"
lattice_type = "hcp"
temperature = 80    # Units: K
reference = "Chesser, N.J., Axe, J.D.: Phys. Rev. B9 (1974) 4060"
details = "The model is of the 'modified axially symmetric' form. Force constants obtained by a fit to the phonon frequencies and the relative phase of the two hexagonal sublattices for the [100] longitudinal (T) phonon modes."
a = 2.66   # lattice parameters in angstroms
c = 4.95

# Units: N m^-1 
force_constants = { "1" : { "K" : 10.150,
                            "C_Bx" : -0.594,
                            "C_Bz" : -2.003 },
                    "2" : { "K" : 29.235,
                            "C_Bx" : -3.484,
                            "C_Bz" : -3.347 },
                    "3" : { "K" : 3.004,
                            "C_Bx" : -0.145,
                            "C_Bz" : 0.803 },
                    "4" : { "K + C_Bz" : -0.075,
                            "C_Bx" : 0.162 },
                    "5" : { "K" : -0.3531,
                            "C_Bx" : 0.309,
                            "C_Bz" : -0.011 },
                    "6" : { "K" : 2.264,
                            "C_Bx" : -0.104,
                            "C_Bz" : 1.051 } }
