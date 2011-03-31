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
    return map(importShapeType, shapenames)


def importShapeType(name):
    pkg = 'vnfb.dom.geometry'
    m = '%s.%s' % (pkg, name)
    m = _import(m)
    return getattr(m, name)


def _import(m):
    return __import__(m, {}, {}, [''])
        

# version
__id__ = "$Id$"

# End of file 
