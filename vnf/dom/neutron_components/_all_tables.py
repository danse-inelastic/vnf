thispackage = 'vnf.dom.neutron_components'

def tables():
    tablenames = [
        ]
    
    tables = [
        getattr(_import('%s.%s' % (thispackage, name)), name)
        for name in tablenames ]
              
    return tables


def _import(package):
    return __import__(package, {}, {}, [''])
