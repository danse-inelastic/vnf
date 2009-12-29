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


from _ import o2t as object2table


def importType(name):
    path = name.split('.')
    m = '.'.join(path[:-1])
    m = _import(m)
    return getattr(m, path[-1])


def _import(modulename):
    pkg = 'vnfb.dom'
    m = '%s.%s' % (pkg, modulename)
    return __import__(m, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
