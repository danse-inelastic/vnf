# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


def block():
    from Block import Block
    return Block()


def configure_arcs_simple_instrument():
    from ARCS_simple import ARCS_simple
    return ARCS_simple()


def configure_sans_ng7_instrument():
    from SANS_NG7 import SANS_NG7
    return SANS_NG7()


def configureneutronscatterer( formname, mattertype, shapetype ):
    from ConfigureNeutronScatterer import form
    return form( formname, mattertype, shapetype )


# version
__id__ = "$Id$"

# End of file 
