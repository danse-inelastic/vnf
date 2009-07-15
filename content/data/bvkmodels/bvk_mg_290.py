# bvk_ho_290.py
# BvK force constants

element = "Mg"
lattice_type = "hcp"
temperature = 290    # Units: K
reference = "Singh, S.N., Prakash, S.: Physica 50 (1970) 10 and DeWames, R.E., Wolfram, T., Lehman, G.W.: Phys Rev. 138 (1965) A 717"
details = "The model is axially symmetric"

# Units: N m^-1 
force_constants = { "1" : { "f_r" : 10.483,
                            "f_t" : -0.309 },
                    "2" : { "f_r" : 10.099,
                            "f_t" : -0.292 },
                    "3" : { "f_r" : -0.222,
                            "f_t" : -0.246 },
                    "4" : { "f_r" : 0.305,
                            "f_t" : -0.490 },
                    "5" : { "f_r" : 0.748,
                            "f_t" : 0.013 },
                    "6" : { "f_r" : 0.529,
                            "f_t" : 0.091 },
                    "7" : { "f_r" : -0.049,
                            "f_t" : 0.157 },
                    "8" : { "f_r" : -0.401,
                            "f_t" : 0.042 } }
