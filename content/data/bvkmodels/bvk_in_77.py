# bvk_in_77.py
# BvK force constants

element = "In"
lattice_type = "fct"
temperature = 77    # Units: K
reference = "Smith, H.G., Reichardt, W.: Bull. Am. Phy. Soc. 14 (1969) 378 (unpublished)"
a = 4.58   # lattice parameters in angstroms
c = 4.94

# Units: N m^-1 
force_constants = { "101" : { "f_r" : 12.316,
                              "f_t" : -2.064 },
                    "110" : { "f_r" : 16.763,
                              "f_t" : -2.759 },
                    "200" : { "f_r" : 1.278,
                              "f_t" : 0.929 },
                    "002" : { "f_r" : 1.695,
                              "f_t" : 0.294 },
                    "211" : { "f_r" : -0.452,
                              "f_t" : 0.002 },
                    "112" : { "f_r" : -0.601,
                              "f_t" : 0.268 },
                    "202" : { "f_r" : -0.423,
                              "f_t" : -0.216 },
                    "220" : { "f_r" : -1.130,
                              "f_t" : 0.033 },
                    "310" : { "f_r" : 0.167 },
                    "103" : { "f_r" : -0.026 },
                    "301" : { "f_r" : 0.225 } }
