
def tables():
    instrument = [
        ]


    kernels = [
        'PolyXtalCoherentPhononScatteringKernel',
        ]


    kernel_related = [
        'PhononDOS',
        'PhononDispersion',
        'BvKComputation',
        'BvKModel',
        'VacfComputation',
        ]

    
    other = [
        ]
    
    
    tablemodules = \
                 kernels \
                 + kernel_related \
                 + instrument \
                 + other
    
    tables = []
    for t in tablemodules:
        exec 'from vnf.dom.ins.%s import %s as table' % (t, t) in locals()
        tables.append(table)
        continue

    return tables

