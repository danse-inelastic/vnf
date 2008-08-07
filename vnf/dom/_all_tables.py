
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
    'Sample',
    ]


other = [
    'User',
    'Server',
    'Job',
    ]


tablemodules = instrument \
         + shapes \
         + sample \
         + other

tables = []
for t in tablemodules:
    exec 'from %s import %s as table' % (t, t) in locals()
    tables.append( table )
    continue


