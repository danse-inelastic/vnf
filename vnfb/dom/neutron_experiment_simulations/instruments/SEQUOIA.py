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
        name='SEQUOIA',
        short_description='SEQUOIA. place holder',
        long_description='long description here',
        category='ins',
        creator='vnf', date='08/11/2008',
        components=[],
        status = 'offline',
        )


from _utils import ccomp, cinstr


# version
__id__ = "$Id$"

# End of file 
