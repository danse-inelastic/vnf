# bvk_sc_295.py
# BvK force constants

element = "Sc"
lattice_type = "hcp"
temperature = 295    # Units: K
reference = "Singh, S.N., Prakash, S.: Physica 50 (1970) 10"
details = "The model is of the 'modified axially symmetric form'."
a = 3.31   # lattice parameters in angstroms
c = 5.27

# Units: N m^-1 
force_constants = { "1" : { "K" : 23.198,
                            "C_Bx" : -2.576,
                            "C_Bz" : 1.981 },
                    "2" : { "K" : 11.793,
                            "C_Bx" : 2.374,
                            "C_Bz" : 1.525 },
                    "3" : { "K" : -9.944,
                            "C_Bx" : 2.284,
                            "C_Bz" : 1.981 },
                    "4" : { "K + C_Bz" : -0.610,
                            "C_Bx" : -0.622 },
                    "5" : { "K" : 3.557,
                            "C_Bx" : 0.539,
                            "C_Bz" : -0.648 },
                    "6" : { "K" : 1.307,
                            "C_Bx" : -0.041,
                            "C_Bz" : -0.115 } }

