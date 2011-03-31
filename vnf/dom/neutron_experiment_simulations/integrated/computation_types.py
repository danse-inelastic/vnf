# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


typenames = [
    'neutron_experiment_simulations.integrated.arcs.ARCSbeam.ARCSbeam',
    ]


deps_typenames = [
    ]


def getTypes():
    from vnf.dom import importType
    return map(importType, typenames)


# version
__id__ = "$Id$"

# End of file 
