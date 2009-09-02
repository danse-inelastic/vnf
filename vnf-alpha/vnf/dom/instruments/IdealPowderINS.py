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


from vnf.dom.neutron_components.MonochromaticSource import MonochromaticSource
from vnf.dom.neutron_components.SampleComponent import SampleComponent
from vnf.dom.neutron_components.QEMonitor import QEMonitor



def source():
    c = MonochromaticSource()
    c.id = new_id()
    c.energy = 70
    return c
    

def monitor():
    c = QEMonitor()
    c.id = new_id()
    
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
    c.id = new_id()
    return c


def create(db):
    componentinfos = [
        ci('source', source(), ( (0,0,0), (0,0,0), '' ) ),
        ci('sample', sample(), ( (0,0,3), (0,0,0), '' ) ),
        ci('monitor', monitor(), ( (0,0,3), (0,0,0), '' ) ),
        ]
    
    newInstrument(
        db=db,
        id='IdealPowderINS',
        short_description='Ideal INS instrument for powder sample',
        long_description='''Ideal inelastic neutron scattering instrument for powder sample''',
        category='ins',
        creator='vnf',
        date='12/16/2008',
        componentinfos=componentinfos,
        )
    
    return


from _utils import new_id, newInstrument, componentinfo as ci


# version
__id__ = "$Id$"

# End of file 
