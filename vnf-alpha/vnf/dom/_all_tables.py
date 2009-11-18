
main_dom = 'vnf.dom'

# handle to which external dom extension can be added
# an extension is a python package. it should have a method "alltables" which
# returns a list of tables provided by that package.
external_dom_extensions = []


acl = [
    'User',
    'Role',
    'ACL1',
    'ACL2',
    ]

instrument = [
    'Instrument',
    'InstrumentConfiguration',
    ]


acl2 = [
    'ACL_InstrumentSimulationPrivilege',
    ]


shapes = [
    'Block',
    'Cylinder',
    ]


materials = [
    'Atom',
    'Lattice',
    'AtomicStructure',
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
    'PhononsFromAbinitio',
    'GulpSimulation',
    'MmtkSimulation',
    'MdAnalysis',
    ]


kernel_related = [
    'GulpPotential'
    ]


other = [
    'Registrant',
    'Server',
    'Job',
    'ITask',
    'Activity',
    'SmartLabel',
    'Label',
    'TransientObject',
    ]


tablemodules = \
             acl \
             + shapes \
             + materials \
             + kernels \
             + kernel_related \
             + sample \
             + instrument \
             + acl2 \
             + experiment \
             + other


def tables():
    # tables in this package

    tables = []

    #   hidden tables
    from _hidden_tables import tables as _hidden_tables
    tables += _hidden_tables()
    
    #   normal tables
    for t in tablemodules:
        m = '%s.%s' % (main_dom, t)
        module = _import(m)
        table = getattr(module, t)
        tables.append( table )
        continue

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
