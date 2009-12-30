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

from vnfb.dom.neutron_experiment_simulations.neutron_components.MonochromaticSource import MonochromaticSource
from vnfb.dom.neutron_experiment_simulations.neutron_components.TofMonitor import TofMonitor



def source():
    c = MonochromaticSource()
    c.energy = 47.043
    return c
    

def monitor():
    c = TofMonitor()
    c.tmin = 0
    c.tmax = 2e-3
    return c



def create(orm):
    componentinfos = [
        ci('source', source(), ( (0,0,0), (0,0,0), '' ) ),
        ci('monitor', monitor(), ( (0,0,3), (0,0,0), '' ) ),
        ]
    
    newInstrument(
        orm,
        short_description='Test instrument (monochromatic source and a tof monitor)',
        long_description='''Test instrument (monochromatic source and a tof monitor)''',
        category='Test',
        creator='vnf',
        date='11/24/2008',
        componentinfos=componentinfos,
        )
    
    return


from _utils import newInstrument, componentinfo as ci


# version
__id__ = "$Id$"

# End of file 
