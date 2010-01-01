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

from vnfb.dom.neutron_experiment_simulations.neutron_components.MonochromaticSource import MonochromaticSource
from vnfb.dom.neutron_experiment_simulations.neutron_components.SampleComponent import SampleComponent
from vnfb.dom.neutron_experiment_simulations.neutron_components.QMonitor import QMonitor



def source():
    c = MonochromaticSource()
    return c
    

def sample():
    c = SampleComponent()
    return c


def detector():
    c = QMonitor()
    return c



def createInstrument(director):
    components = [
        ccomp('source', source(), ( (0,0,0), (0,0,0), '' ) ),
        ccomp('sample', sample(), ( (0,0,0), (0,0,0), '' ) ),
        ccomp('detector', detector(), ( (0,0,0), (0,0,0), '' ) ),
        ]
    
    return cinstr(
        director,
        name='SANS_NG7',
        short_description='NIST NG7',
        long_description='''NG7 30-m Small Angle Neutron Scattering Instrument''',
        category='sans',
        creator='vnf',
        date='08/24/2008',
        components=components,
        status = 'offline',
        )
    

from _utils import ccomp, cinstr


# version
__id__ = "$Id$"

# End of file 
