# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


kernelnames = [
    'ins.PolyXtalCoherentPhononScatteringKernel.PolyXtalCoherentPhononScatteringKernel',
    'ins.SQEKernel.SQEKernel',
    'sans.SANSSphereModelKernel.SANSSphereModelKernel',
    ]


def getKernelTypes():
    pkg = 'vnfb.dom.scattering_kernels'

    def _(n):
        path = n.split('.')
        m = '%s.%s' % (pkg, '.'.join(path[:-1]))
        m = _import(m)
        return getattr(m, path[-1])
        
    return map(_, kernelnames)


def _import(m):
    return __import__(m, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
