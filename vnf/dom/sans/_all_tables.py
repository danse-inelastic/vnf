
def tables():
    instrument = [
        ]


    kernels = [
        'SANSSphereModelKernel',
        ]


    kernel_related = [
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
        exec 'from vnf.dom.sans.%s import %s as table' % (t, t) in locals()
        tables.append( table )
        continue

    return tables

