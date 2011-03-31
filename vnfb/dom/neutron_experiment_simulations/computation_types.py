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
    'neutron_experiment_simulations.NeutronExperiment.NeutronExperiment',
    ]

from integrated.computation_types import typenames as ts
typenames += ts


deps_typenames = [
    'neutron_experiment_simulations.NeutronStorage.NeutronStorage',
    ]


def getTypes():
    from vnfb.dom import importType
    return map(importType, typenames)


# version
__id__ = "$Id$"

# End of file 
