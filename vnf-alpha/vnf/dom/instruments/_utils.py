def new_id():
    from vnf.dom.idgenerator import generator
    return generator()


def newInstrument(db, id, short_description, long_description, category, creator, date, componentinfos, status='online'):

    from vnf.dom.Instrument import Instrument
    
    r = Instrument()
    r.id = id
    r.short_description = short_description
    r.long_description = long_description
    r.category = category
    r.creator = creator
    r.date = date
    r.status = status

    components_proxy = r.components
    geometer_proxy = r.geometer
    componentsequence = r.componentsequence = []
    
    for componentinfo in componentinfos:
        
        name = componentinfo.name
        component = componentinfo.component
        pinfo = componentinfo.positionalinfo
        
        db.insertRow( component )
        components_proxy.add( component, db, name )
        
        geometer_proxy.register(
            name,
            position = pinfo.position, orientation = pinfo.orientation,
            reference = pinfo.reference,
            db = db)

        componentsequence.append( name )
        continue

    db.insertRow( r )
    return r
    


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
