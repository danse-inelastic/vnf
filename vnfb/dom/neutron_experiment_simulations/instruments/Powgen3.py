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
    cinstr(
        director,
        name='Powgen3',
        short_description='Powgen3. place holder',
        long_description='long description here',
        category='diffraction',
        creator='vnf', date='08/11/2008',
        components=[],
        status = 'offline',
        )
    return


from _utils import ccomp, cinstr


# version
__id__ = "$Id$"

# End of file 
