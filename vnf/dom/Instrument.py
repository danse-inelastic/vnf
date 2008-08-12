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
    
    pass # end of Instrument


def inittable(db):
    def add(id, short_description, category, creator, date, components):
        r = Instrument()
        r.id = id
        r.short_description = short_description
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

    from MonochromaticSource import MonochromaticSource
    from IQEMonitor import IQEMonitor
    from SampleComponent import SampleComponent
    
    add( 'ARCS_simple', 'simplified ARCS',
         'direct-geometry time-of-flight chopper spectrometer',
         'vnf', '08/09/2008',
         [  ('source', MonochromaticSource, ( (0,0,0), (0,0,0), '' ) ),
            ('sample', SampleComponent, ( (0,0,0), (0,0,0), '' ) ),
            ('detector', IQEMonitor, ( (0,0,0), (0,0,0), '' ) ),
            ]
         )

    add( 'Pharos', 'Pharos. place holder',
         'direct-geometry time-of-flight chopper spectrometer',
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
