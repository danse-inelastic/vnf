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
    'name': 'VULCAN',
    'short_description': 'SNS diffractometer',
    'long_description': 'VULCAN is a diffractometer at the Spallation Neutron Source intended for measurements of deformation, residual stress related studies, spatial mapping of chemistry, microstructure, and texture.',
    'category': 'engineering diffraction',
    'creator': 'vnf',
    'date': '9/11/2010',
    'components': components,
    }


#def createInstrument(director):
#    return cinstr(
#        director,
#        name='VULCAN',
#        short_description='VULCAN. place holder',
#        long_description='long description here',
#        category='engineering diffraction',
#        creator='vnf', date='08/11/2008',
#        components=[],
#        )


from _utils import ccomp, cinstr


# version
__id__ = "$Id$"

# End of file 
