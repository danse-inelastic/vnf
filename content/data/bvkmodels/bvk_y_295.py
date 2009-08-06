# bvk_y_295.py
# BvK force constants

element = "Y"
lattice_type = "hcp"
temperature = 295    # Units: K
reference = "Sinha, S.K., Brun, T.O., Muhlestein, L.D., Sakurai, J.: Phys. Rev. B 1 (1970) 2430"
details = "The model is of the 'modified axially symmetric' form."
a = 3.65   # lattice parameters in angstroms
c = 5.73

# Units: N m^-1 
force_constants = { "1" : { "K" : 23.239,
                            "C_Bx" : -1.628,
                            "C_Bz" : -3.641 },
                    "2" : { "K" : 10.124,
                            "C_Bx" : 1.456,
                            "C_Bz" : 0.150 },
                    "3" : { "K" : -6.393,
                            "C_Bx" : 1.212,
                            "C_Bz" : 1.511 },
                    "4" : { "K + C_Bz" : -0.083,
                            "C_Bx" : -0.178 },
                    "5" : { "K" : 1.392,
                            "C_Bx" : 0.456,
                            "C_Bz" : -0.582 },
                    "6" : { "K" : 1.856,
                            "C_Bx" : -0.093,
                            "C_Bz" : 0.593 } }

