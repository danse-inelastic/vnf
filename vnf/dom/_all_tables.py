
main_dom = 'vnf.dom'

# handle to which external dom extension can be added
# an extension is a python package. it should have a method "alltables" which
# returns a list of tables provided by that package.
external_dom_extensions = []


instrument = [
    'Instrument',
    'InstrumentConfiguration',
    ]


shapes = [
    'Block',
    'Cylinder',
    ]


materials = [
    'PolyCrystal',
    'SingleCrystal',
    'Disordered',
    ]


sample = [
    'Scatterer',
    'ScattererExample',
    'Sample',
    'SampleAssembly',
    'SampleEnvironment',
    ]


experiment = [
    'NeutronExperiment',
    ]


kernels = [
    'AbInitio',
    ]


kernel_related = [
    ]


other = [
    'User',
    'Server',
    'Job',
    ]


tablemodules = \
             shapes \
             + materials \
             + kernels \
             + kernel_related \
             + sample \
             + instrument \
             + experiment \
             + other


def tables():
    # tables in this package
    #   normal tables
    tables = []
    for t in tablemodules:
        m = '%s.%s' % (main_dom, t)
        module = _import(m)
        table = getattr(module, t)
        tables.append( table )
        continue
    #   hidden tables
    from _hidden_tables import tables as _hidden_tables
    tables += _hidden_tables()

    # other dom packages in standard places
    domexts = []
    from vnf import extensions
    domexts += extensions
    domexts.append('neutron_components')
    dompackages = [_get_standard_extension(ext) for ext in domexts]

    # additional external doms
    dompackages += external_dom_extensions

    # add all dom packages
    for package in dompackages: _add_tables_from_package(package, tables) 
    
    return tables


def children( base ):
    'find child tables of given base'
    return filter(lambda t: issubclass(t, base), tables())




# implementations
def _add_tables_from_package(package, tables):
    new = package.alltables()
    tables += new
    return tables


def _get_standard_extension(ext):
    package = '%s.%s' % (main_dom, ext)
    return _import( package)


def _import(package):
    return __import__(package, {}, {}, [''])
