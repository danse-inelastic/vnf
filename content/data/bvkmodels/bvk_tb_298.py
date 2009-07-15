# bvk_tb_298.py
# BvK force constants

element = "Tb"
lattice_type = "hcp"
temperature = 298    # Units: K
reference = "Houmann, J.C.G., Nicklow, R.M.: Phys. Rev. B1 (1970) 3943"
details = "The model is axially symmetric from the fifth neighbours outward"

# Units: N m^-1 
force_constants = { "1" : { "xx" : 5.467,
                            "yy" : 1.562,
                            "zz" : 9.901,
                            "xz" : 7.286 },
                    "2" : { "xx" : 0.954,
                            "yy" : 11.416,
                            "zz" : -0.952,
                            "xy" : 2.426 },
                    "3" : { "xx" : -1.889,
                            "yy" : -0.975,
                            "zz" : -0.894,
                            "xz" : 0.046 },
                    "4" : { "xx" : -0.032,
                            "zz" : -2.228 },
                    "5" : { "f_r" : 1.225,
                            "f_t" : -0.180 },
                    "6" : { "f_r" : 1.250,
                            "f_t" : 0.241,
                    "7" : { "f_r" : 0.762,
                            "f_t" : -0.098 },
                    "8" : { "f_r" : -0.410,
                            "f_t" : 0.066 } } 

