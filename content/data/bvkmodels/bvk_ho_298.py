# bvk_ho_298.py
# BvK force constants

element = "Ho"
lattice_type = "hcp"
temperature = 298    # Units: K
reference = "Nicklow, R.M., Wakabayashi, N., Vijayaraghavan, P.R.: Phys. Rev. B3 (1971) 1229"
details = "Axially symmetric from the fifth neighbours outward"

# Units: N m^-1 
force_constants = { "1" : { "xx" : 7.054,
                            "yy" : 1.055,
                            "zz" : 11.517,
                            "xz" : 6.766 },
                    "2" : { "xx" : 1.084,
                            "yy" : 12.716,
                            "zz" : -0.927,
                            "xy" : 2.259 },
                    "3" : { "xx" : -1.496,
                            "yy" : -0.937,
                            "zz" : -1.066,
                            "xz" : 0.965 },
                    "4" : { "xx" : 0.080,
                            "zz" : -3.897 },
                    "5" : { "f_r" : 0.488,
                            "f_t" : -0.011 },
                    "6" : { "f_r" : 1.213,
                            "f_t" : 0.318 },
                    "7" : { "f_r" : 1.048,
                            "f_t" : -0.133 },
                    "8" : { "f_r" : -0.344,
                            "f_t" : 0.040 } } 




