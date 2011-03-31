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


from vnf.dom.neutron_experiment_simulations.neutron_components.MonochromaticSource import MonochromaticSource
from vnf.dom.neutron_experiment_simulations.neutron_components.SampleComponent import SampleComponent
from vnf.dom.neutron_experiment_simulations.neutron_components.QEMonitor import QEMonitor



def source():
    c = MonochromaticSource()
    c.energy = 70
    return c
    

def monitor():
    c = QEMonitor()
    
    c.Emin = -50
    c.Emax = 50
    c.nE = 100

    c.Qmin = 0
    c.Qmax = 13
    c.nQ = 130

    c.max_angle_in_plane = 120
    c.min_angle_in_plane = -30
    c.max_angle_out_of_plane = 30
    c.min_angle_out_of_plane = -30
    
    return c


def sample():
    c = SampleComponent()
    return c


def createInstrument(director):
    components = [
        ccomp('source', source(), ( (0,0,0), (0,0,0), '' ) ),
        ccomp('sample', sample(), ( (0,0,3), (0,0,0), '' ) ),
        ccomp('monitor', monitor(), ( (0,0,3), (0,0,0), '' ) ),
        ]
    
    return cinstr(
        director,
        name='IdealPowderINS',
        short_description='Ideal INS instrument for powder sample',
        long_description='''Ideal inelastic neutron scattering instrument for powder sample''',
        category='ins',
        creator='vnf',
        date='12/16/2008',
        components=components,
        )
    


from _utils import ccomp, cinstr


# version
__id__ = "$Id$"

# End of file 
