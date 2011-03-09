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
    'scattering_kernels.IsotropicElasticKernel.IsotropicElasticKernel',
    'scattering_kernels.ins.PolyXtalCoherentPhononScatteringKernel.PolyXtalCoherentPhononScatteringKernel',
    'scattering_kernels.ins.SQEKernel.SQEKernel',
    'scattering_kernels.diff.PowderDiffractionKernel.PowderDiffractionKernel',
    #'sans.SANSSphereModelKernel.SANSSphereModelKernel',
    ]


def getKernelTypes():
    from vnfb.dom import importType
    return map(importType, kernelnames)


def _import(m):
    return __import__(m, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
