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


shapenames = [
    'Block',
    'Cylinder',
    ]


def getShapeTypes():
    pkg = 'vnfb.dom.geometry'

    def _(n):
        m = '%s.%s' % (pkg, n)
        m = _import(m)
        return getattr(m, n)
        
    return map(_, shapenames)


def _import(m):
    return __import__(m, {}, {}, [''])
        

# version
__id__ = "$Id$"

# End of file 
