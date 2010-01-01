# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


# a test instrument with only two components


components = [
    ('source',
     ('MonochromaticSource', {'energy': 47.043}),
     ( (0,0,0), (0,0,0), '' )
     ),
    ('monitor',
     ('TofMonitor', {'tmin':0, 'tmax': 2e-3}),
     ( (0,0,3), (0,0,0), '' )
     ),
    ]

instrument = {
    'name': 'Test',
    'short_description': 'Test',
    'long_description': 'Test instrument (monochromatic source and a tof monitor)',
    'category': 'Test',
    'creator': 'vnf',
    'date': '11/24/2008',
    'components': components,
    }


# version
__id__ = "$Id$"

# End of file 
