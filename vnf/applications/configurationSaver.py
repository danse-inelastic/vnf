

def retrieveConfiguration(inventory, registry):
    """place the current inventory configuration in the given registry"""
    
    from pyre.inventory.Facility import Facility
    from pyre.inventory.Property import Property
    from journal.components.Journal import Journal
    
    node = registry.getNode(inventory._priv_name)
    
    for prop in inventory.properties():
        
        name = prop.name
        descriptor = inventory.getTraitDescriptor(name)
        value = descriptor.value
        locator = descriptor.locator
        
        if name == "weaver": continue
        #if isinstance(prop, Property) and value == prop.default: continue
        if isinstance(prop, Facility) and isinstance(value, Journal): continue
        if value and isinstance(prop, Facility): value = value.name
        
        node.setProperty(name, value, locator)
        continue
    
    for fac in inventory.facilities():
        component = fac.__get__(inventory)
        if isinstance(component, Journal): continue
        if component is None:
            raise RuntimeError, "Unable to retrieve component for facility %s" % fac.name
        retrieveConfiguration(component.inventory, node)
        continue
    
    return registry



def toPml(pyreapp, path):
    registry = pyreapp.createRegistry()
    registry = retrieveConfiguration( pyreapp.inventory, registry )
    stream = open(path, 'w')
    weaver = pyreapp.inventory.weaver
    renderer = pyreapp.getCurator().codecs['pml'].renderer
    weaver.renderer = renderer
    weaver.weave(registry, stream)
    return

                                                                                                                                                    
