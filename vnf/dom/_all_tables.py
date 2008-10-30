
instrument = [
    'IQEMonitor',
    'IQMonitor',
    'Instrument',
    'MonochromaticSource',
    'SampleComponent',
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

tables = []
for t in tablemodules:
    exec 'from %s import %s as table' % (t, t) in locals()
    tables.append( table )
    continue


from _hidden_tables import tables as _hidden_tables
tables += _hidden_tables()



# tables in extensions
from vnf import extensions
def _get_ext_tables(ext):
    exec 'from vnf.dom.%s import alltables' % ext
    return alltables()
exttableslist = [_get_ext_tables(ext) for ext in extensions]
for exttables in exttableslist:
    tables += exttables



def children( base ):
    'find child tables of given base'
    r = []
    for table in tables:
        if issubclass( table, base ): r.append( table )
        continue
    return r
