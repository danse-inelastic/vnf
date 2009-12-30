
def createInstrument(
    instrumentinfo,
    orm,
    ):

    from vnfb.dom.neutron_experiment_simulations.Instrument import Instrument
    from vnfb.dom.neutron_experiment_simulations.GeometricalRelation import GeometricalRelation
    
    
    instrument = Instrument()
    instrument.short_description = instrumentinfo['short_description']
    instrument.long_description = instrumentinfo['long_description']
    instrument.category = instrumentinfo['category']

    components = []; instrument.components = components
    geo_relations = []; instrument.geometrical_relations = geo_relations
    
    for name, (type, kwds), (position, orientation, reference) \
            in instrumentinfo['components']:
        
        component = createComponent(type, kwds)
        components.append(component)

        geo_relation = GeometricalRelation()
        geo_relation.targetname = name
        geo_relation.position = position
        geo_relation.orientation = _tomatrix(orientation)
        geo_relation.referencename = reference
        geo_relations.append(geo_relation)
        continue

    orm.save(instrument)
    r = orm(instrument)
    
    r.creator = instrumentinfo['creator']
    r.date = instrumentinfo['date']
    r.status = instrumentinfo.get('status') or 'online'
    orm.db.updateRecord(r)
    
    return instrument


import numpy as np
from mcni.neutron_coordinates_transformers import mcstasRotations
def _tomatrix(orientation):
    orientation = np.array(orientation)
    if orientation.size==3:
        return mcstasRotations.toMatrix(*orientation)
    elif orientation.size==9:
        orientation.shape =3,3
        return orientation
    raise ValueError, str(orientation)


def createComponent(typename, kwds):
    t = 'neutron_experiment_simulations.neutron_components.%s.%s' % (typename, typename)
    from vnfb.dom import importType
    t = importType(t)
    o = t()
    for k,v in kwds.iteritems():
        setattr(o, k, v)
    return o



