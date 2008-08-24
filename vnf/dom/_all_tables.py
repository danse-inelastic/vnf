
instrument = [
    'Instrument',
    'MonochromaticSource',
    'IQMonitor',
    'IQEMonitor',
    'SampleComponent',
    'ARCS_simple',
    'SANS_NG7',
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
    'Sample',
    'SampleAssembly',
    'SampleEnvironment',
    ]


experiment = [
    'NeutronExperiment',
    ]


kernels = [
    'IDFPhononDispersion',
    'PolyXtalCoherentPhononScatteringKernel',
    'SANSSphereModelKernel',
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
             + sample \
             + instrument \
             + experiment \
             + other

tables = []
for t in tablemodules:
    exec 'from %s import %s as table' % (t, t) in locals()
    tables.append( table )
    continue


from _hidden_tables import tables as _hidden_tables
tables += _hidden_tables()


def children( base ):
    'find child tables of given base'
    r = []
    for table in tables:
        if issubclass( table, base ): r.append( table )
        continue
    return r
