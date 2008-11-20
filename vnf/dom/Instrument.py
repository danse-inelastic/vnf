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



from OwnedObject import OwnedObject
class Instrument(OwnedObject):
    
    name = "instruments"
    
    import vnf.dom
    components = vnf.dom.referenceSet( name = 'components' )
    
    import pyre.db
    componentsequence = pyre.db.varcharArray(
        name = 'componentsequence', length = 128, default = [] )

    category = pyre.db.varchar( name = 'category', length = 64 )

    import vnf.dom
    geometer = vnf.dom.geometer()

    long_description = pyre.db.varchar( name = 'long_description', length = 8192 )
    
    pass # end of Instrument


def inittable(db):
    def add(id, short_description, long_description, category, creator, date, components):
        r = Instrument()
        r.id = id
        r.short_description = short_description
        r.long_description = long_description
        r.category = category
        r.creator = creator
        r.date = date
        components_proxy = r.components
        geometer_proxy = r.geometer
        componentsequence = r.componentsequence
        
        for name, type, (position, orientation, reference) in components:
            component = type( )
            component.id = new_id()
            db.insertRow( component )
            components_proxy.add( component, db, name )
            geometer_proxy.register( name, position, orientation, db, reference )
            componentsequence.append( name )
            continue
        
        db.insertRow( r )
        return 
    
    from neutron_components.MonochromaticSource import MonochromaticSource
    from neutron_components.SampleComponent import SampleComponent
    from neutron_components.SNSModerator import SNSModerator
    from neutron_components.QEMonitor import QEMonitor
    from neutron_components.QMonitor import QMonitor
    from neutron_components.TofMonitor import TofMonitor
    from neutron_components.ChanneledGuide import ChanneledGuide
    from neutron_components.NeutronRecorder import NeutronRecorder
    from neutron_components.T0Chopper import T0Chopper
    from neutron_components.FermiChopper import FermiChopper
    
    add( 'ARCS_beam', 'ARCS',
         '''ARCS is a wide Angular-Range, direct-geometry, time-of-flight Chopper Spectrometer at the Spallation Neutron Source. It is optimized to provide a high neutron flux at the sample, and a large solid angle of detector coverage.
  This virtual instrument simulates neutrons being emitted from moderator and going through neutron optics of ARCS until they reach the sample position. Those neutrons are then saved and can be used to study inelastic neutron scattering of samples later.
''',
         'ins',
         'vnf', '08/09/2008',
         [  ('source', SNSModerator, ( (0,0,0), (0,0,0), '' ) ),
            ('core_ves', ChanneledGuide, ((0,0,1.0106), (0,0,0), '' ) ),
            ('shutter_guide', ChanneledGuide, ((0,0,2.26790), (0,0,0), '' ) ),
            ('guide_1_1_1', ChanneledGuide, ((0,0,4.17230), (0,0,0), '' ) ),
            ('guide_1_1_2', ChanneledGuide, ((0,0,4.65589), (0,0,0), '' ) ),
            ('guide_1_1_3', ChanneledGuide, ((0,0,5.13948), (0,0,0), '' ) ),
            ('guide_1_2_1', ChanneledGuide, ((0,0,5.62331), (0,0,0), '' ) ),
            ('guide_1_2_2', ChanneledGuide, ((0,0,6.10690), (0,0,0), '' ) ),
            ('guide_1_2_3', ChanneledGuide, ((0,0,6.59049), (0,0,0), '' ) ),
            ('guide_1_3_1', ChanneledGuide, ((0,0,7.07433), (0,0,0), '' ) ),
            ('guide_1_3_2', ChanneledGuide, ((0,0,7.55792), (0,0,0), '' ) ),
            ('guide_1_3_3', ChanneledGuide, ((0,0,8.04145), (0,0,0), '' ) ),
            ('t0_chop', T0Chopper, ((0,0,8.77), (0,0,0), '' ) ),
            ('guide_2_1', ChanneledGuide, ((0,0,9.47504), (0,0,0), '' ) ),
            ('guide_2_2', ChanneledGuide, ((0,0,9.87713), (0,0,0), '' ) ),
            ('guide_2_3', ChanneledGuide, ((0,0,10.27922), (0,0,0), '' ) ),
            ('guide_2_4', ChanneledGuide, ((0,0,10.68131), (0,0,0), '' ) ),
            ('guide_2_5', ChanneledGuide, ((0,0,11.08340), (0,0,0), '' ) ),
            ('fermi_chop', FermiChopper, ((0,0,11.61), (0,0,0), '' ) ),
            ('tofmonitor1', TofMonitor, ((0,0,11.82), (0,0,0), '')),
            ('guide_3', ChanneledGuide, ((0,0,11.84975), (0,0,0), '' ) ),
            ('guide_4_1', ChanneledGuide, ((0,0,12.08825), (0,0,0), '' ) ),
            ('guide_4_2', ChanneledGuide, ((0,0,12.55105), (0,0,0), '' ) ),
            ('guide_5', ChanneledGuide, ((0,0,13.01830), (0,0,0), '' ) ),
            ('neutron_recorder', NeutronRecorder, ((0,0,13.5), (0,0,0), '')),
            ]
         )

    add( 'SANS_NG7', 'NIST NG7',
         '''NG7 30-m Small Angle Neutron Scattering Instrument''',
         'sans',
         'vnf', '08/24/2008',
         [  ('source', MonochromaticSource, ( (0,0,0), (0,0,0), '' ) ),
            ('sample', SampleComponent, ( (0,0,0), (0,0,0), '' ) ),
            ('detector', QMonitor, ( (0,0,0), (0,0,0), '' ) ),
            ]
         )

    add( 'SEQUOIA', 'SEQUOIA. place holder',
         'long description here',
         'ins',
         'vnf', '08/11/2008',
         []
         )
    
    add( 'Pharos', 'Pharos. place holder',
         'long description here',
         'ins',
         'vnf', '08/11/2008',
         []
         )
    
    add( 'Powgen3', 'Powgen3. place holder',
         'long description here',
         'diffraction',
         'vnf', '08/11/2008',
         []
         )
    
    add( 'VULCAN', 'VULCAN. place holder',
         'long description here',
         'engineering diffraction',
         'vnf', '08/11/2008',
         []
         )
    
    return


def new_id():
    from idgenerator import generator
    return generator()


# version
__id__ = "$Id$"

# End of file 
