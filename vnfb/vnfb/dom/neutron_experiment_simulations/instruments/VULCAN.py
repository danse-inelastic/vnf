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


def createInstrument(director):
    return cinstr(
        director,
        name='VULCAN',
        short_description='VULCAN. place holder',
        long_description='long description here',
        category='engineering diffraction',
        creator='vnf', date='08/11/2008',
        components=[],
        )


from _utils import ccomp, cinstr


# version
__id__ = "$Id$"

# End of file 
