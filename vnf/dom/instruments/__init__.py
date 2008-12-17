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


thispackage = 'vnf.dom.instruments'

instruments = [
    'ARCS_beam',
    'IdealPowderINS',
    'SANS_NG7',
    'SEQUOIA',
    'Pharos',
    'Powgen3',
    'VULCAN',
    'Test',
    ]


def initall(db):
    modules = [_import('%s.%s' % (thispackage, name)) for name in instruments]
    for m in modules: m.create(db)
    return
    

def _import(package):
    return __import__(package, {}, {}, [''])


# version
__id__ = "$Id$"

# End of file 
