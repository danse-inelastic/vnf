# bvk_cr_300.py
# BvK force constants

element = "Cr"
lattice_type = "bcc"
temperature = 300    # Units: K
reference = ""
details = "Apart from the anomalies, a fourth neighbor fit reproduces the dispersion within 3%. The stron gmaximum in [00?]L direction indicates a strong second neighbour force constant."

# Units: N m^-1 
force_constants = { "111": { "xx": 13.526, 
                             "xy": 6.487 }, 
                    "200": { "xx": 35.915,
                             "yy": -1.564 },
                    "220": { "xx": 2.042,
                             "zz": -0.050,
                             "xy": 2.871 },
                    "311": { "xx": -1.257,
                             "yy": 0.432,
                             "yz": 0.516,
                             "xy": 0.007 } }
