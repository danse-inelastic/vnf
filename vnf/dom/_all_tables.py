
instrument = [
    'Instrument',
    'MonochromaticSource',
    'IQEMonitor',
    ]


shapes = [
    'Block',
    'Cylinder',
    ]


sample = [
    'Scatterer',
    'Sample',
    'SampleAssembly',
    ]


experiment = [
    'NeutronExperiment',
    ]


other = [
    'User',
    'Server',
    'Job',
    ]


tablemodules = instrument \
         + shapes \
         + sample \
         + experiment \
         + other

tables = []
for t in tablemodules:
    exec 'from %s import %s as table' % (t, t) in locals()
    tables.append( table )
    continue


def children( base ):
    'find child tables of given base'
    r = []
    for table in tables:
        if issubclass( table, base ): r.append( table )
        continue
    return r
