
def newInstrument(
    orm,
    short_description, long_description, category, creator, date, componentinfos,
    status='online'):

    from vnfb.dom.neutron_experiment_simulations.Instrument import Instrument
    from vnfb.dom.neutron_experiment_simulations.GeometricalRelation import GeometricalRelation
    
    
    instrument = Instrument()
    instrument.short_description = short_description
    instrument.long_description = long_description
    instrument.category = category

    components = []; instrument.components = components
    geo_relations = []; instrument.geometrical_relations = geo_relations
    
    for componentinfo in componentinfos:
        
        name = componentinfo.name
        component = componentinfo.component
        pinfo = componentinfo.positionalinfo

        components.append(component)

        geo_relation = GeometricalRelation()
        geo_relation.targetname = name
        geo_relation.position = pinfo.position
        geo_relation.orientation = pinfo.orientation
        geo_relation.referencename = pinfo.reference
        geo_relations.append(geo_relation)
        continue

    orm.save(instrument)
    r = orm(instrument)
    
    r.creator = creator
    r.date = date
    r.status = status
    orm.db.updateRecord(r)
    
    return instrument
    


class ComponentInfo:

    name = ''
    component = None
    postionalinfo = None


class PositionalInfo:

    reference = ''
    position = (0,0,0)
    orientation = (0,0,0)


def componentinfo(name, component, positionalinfo):
    position, orientation, reference = positionalinfo
    pi = PositionalInfo()
    pi.reference = reference
    pi.position = position
    pi.orientation = orientation
    
    ci = ComponentInfo()
    ci.name = name
    ci.component = component
    ci.positionalinfo = pi
    return ci
