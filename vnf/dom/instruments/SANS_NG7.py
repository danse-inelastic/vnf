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
from vnf.dom.neutron_components.QMonitor import QMonitor



def source():
    c = MonochromaticSource()
    c.id = new_id()
    return c
    

def sample():
    c = SampleComponent()
    c.id = new_id()
    return c


def detector():
    c = QMonitor()
    c.id = new_id()
    return c



def create(db):
    componentinfos = [
        ci('source', source(), ( (0,0,0), (0,0,0), '' ) ),
        ci('sample', sample(), ( (0,0,0), (0,0,0), '' ) ),
        ci('detector', detector(), ( (0,0,0), (0,0,0), '' ) ),
        ]
    
    newInstrument(
        db=db,
        id='SANS_NG7',
        short_description='NIST NG7',
        long_description='''NG7 30-m Small Angle Neutron Scattering Instrument''',
        category='sans',
        creator='vnf',
        date='08/24/2008',
        componentinfos=componentinfos,
        )
    
    return


from _utils import new_id, newInstrument, componentinfo as ci


# version
__id__ = "$Id$"

# End of file 
