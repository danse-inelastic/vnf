
def tables():
    instrument = [
        ]


    kernels = [
        ]


    kernel_related = [
        ]

    
    other = [
        'SinIQModel',
        'SimpleIQComputation',
        ]
    
    
    tablemodules = \
                 kernels \
                 + kernel_related \
                 + instrument \
                 + other
    
    tables = []
    for t in tablemodules:
        exec 'from vnf.dom.tutorials.%s import %s as table' % (t, t) in locals()
        tables.append( table )
        continue

    return tables

