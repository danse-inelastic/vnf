
def tables():
    instrument = [
        ]


    kernels = [
        #'PolyXtalCoherentPhononScatteringKernel',
        #'SQEKernel',
        ]


    kernel_related = [
        #'PhononDOS',
        #'PhononDispersion',
        #'BvKBond',
        #'BvKComputation',
        #'BvKModel',
        #'SQE',
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
        #print "importing table module %s" % t
        module = '%s.%s' % (package, t)
        module = _import(module)
        table = getattr(module, t)
        tables.append(table)
        continue

    return tables

package = 'vnf.dom.ins'

def _import(module):
    return __import__(module, {}, {}, [''])
