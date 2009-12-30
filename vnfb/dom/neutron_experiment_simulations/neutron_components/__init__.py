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


typenames = [
    'neutron_experiment_simulations.neutron_components.ChanneledGuide.ChanneledGuide',
    ]

def getTypes():
    from vnfb.dom import importType
    return map(importType, typenames)


# version
__id__ = "$Id$"

# End of file 
