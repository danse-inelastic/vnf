# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class JobBuilder:

    def __call__(self, computation, db=None, dds=None, path=None):
        from vnf import extensions as depositories
        Builder = findBuilder(computation.__class__, depositories)
        return Builder(path).render(computation, db=db, dds=dds)
        

def findBuilder(Computation, depositories):
    
    candidates = []
    for depository in depositories:
        package = ['vnf', 'components']
        if depository: package.append(depository)
        package += ['job_builders']
        package = '.'.join(package)

        module = Computation.__name__

        code = 'from %s.%s import Builder' % (package, module)
        try:
            exec code in locals()
        except:
            continue
        candidates.append(Builder)
        continue
    
    l = filter(lambda Builder: Builder.Computation==Computation, candidates)
    if len(l) != 1:
        if not len(l):
            raise RuntimeError, 'No job builder found for computation %s' % Computation
        if len(l) > 1:
            raise RuntimeError, 'More than one job builders for computation %s exist' % Computation
    return l[0]


# version
__id__ = "$Id$"

# End of file 
