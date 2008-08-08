
instrument = [
    'Instrument',
    'MonochromaticSource',
    'IQEMonitor',
    'SampleComponent',
    ]


shapes = [
    'Block',
    'Cylinder',
    ]


materials = [
    'PolyCrystal',
    ]


sample = [
    'Scatterer',
    'Sample',
    'SampleAssembly',
    ]


experiment = [
    'NeutronExperiment',
    ]


kernels = [
    'IDFPhononDispersion',
    'PolyXtalCoherentPhononScatteringKernel',
    ]


other = [
    'User',
    'Server',
    'Job',
    ]


tablemodules = instrument \
         + shapes \
         + materials \
         + sample \
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
