
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
    'ScattererExample',
    'Sample',
    'SampleAssembly',
    'SampleEnvironment',
    ]


experiment = [
    'NeutronExperiment',
    ]


kernels = [
    'PolyXtalCoherentPhononScatteringKernel',
    'SANSSphereModelKernel',
    ]


kernel_related = [
    'IDFPhononDispersion',
    'BvKModel',
    'BvKComputation',
    'PhononDOS',
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
