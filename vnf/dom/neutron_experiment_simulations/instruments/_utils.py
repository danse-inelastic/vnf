
def createInstrument(
    instrumentinfo,
    orm,
    ):
    '''create an instrument from a instrument info dictionary (see Test.py for an example)
    and save it to db by using the given orm
    '''
    from vnf.dom.neutron_experiment_simulations.Instrument import Instrument
    
    instrument = Instrument()
    instrument.name = instrumentinfo['name']
    instrument.short_description = instrumentinfo['short_description']
    instrument.long_description = instrumentinfo['long_description']
    instrument.category = instrumentinfo['category']

    components = []; instrument.components = components
    
    for name, (type, kwds), (position, orientation, reference) \
            in instrumentinfo['components']:
        
        component = createComponent(type, kwds)
        components.append(component)

        component.componentname = name
        component.position = position
        component.orientation = _tomatrix(orientation)
        component.referencename = reference
        continue

    orm.save(instrument)
    r = orm(instrument)
    
    r.creator = instrumentinfo['creator']
    r.date = instrumentinfo['date']
    r.status = instrumentinfo.get('status') or 'online'
    orm.db.updateRecord(r)
    
    return instrument


from vnf.utils.neutron_experiment_simulations.geometry import tomatrix as _tomatrix


def createComponent(typename, kwds):
    t = 'neutron_experiment_simulations.neutron_components.%s.%s' % (typename, typename)
    from vnf.dom import importType
    t = importType(t)
    o = t()
    for k,v in kwds.iteritems():
        setattr(o, k, v)
    return o



# convenient function only for the instrument modules in this subpackage
def ccomp(name, component, geoinfo):
    position, orientation, reference = geoinfo
    component.componentname = name
    component.position = position
    component.orientation = _tomatrix(orientation)
    component.referencename = reference
    return component
    
def cinstr(
    director,
    name, short_description, long_description, category,
    creator, date, components,
    status='online'):
    'name must be unique'
    from _ import Instrument
    instrument = Instrument()
    instrument.short_description = short_description
    instrument.long_description = long_description
    instrument.category = category
    instrument.components = components

    orm = director.clerk.orm
    orm.save(instrument, save_not_owned_referred_object=False)

    r = orm(instrument)
    r.name = name
    r.creator = creator
    r.date = date
    r.status = status
    r.has_sample_component = instrument.hasSampleComponent()
    orm.db.updateRecord(r)

    return instrument
