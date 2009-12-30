typenames = [
    'neutron_experiment_simulations.SampleAssembly.SampleAssembly',
    ]

from samplecomponent_types import typenames as t
typenames+=t

def getTypes():
    from vnfb.dom import importType
    return map(importType, typenames)

