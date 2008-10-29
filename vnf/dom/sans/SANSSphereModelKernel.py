# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from registry import tableRegistry

from ScatteringKernel import ScatteringKernel as base
class SANSSphereModelKernel(base):

    name = 'sansspheremodelkernels'
    
    import pyre.db

    scale = pyre.db.real( name = 'scale', default = 1e-6 )
    radius = pyre.db.real( name = 'radius', default = 60.0 )
    contrast = pyre.db.real( name = 'contrast', default = 1.0 )
    
    pass # end of SANSSphereModelKernel


def inittable(db):
    def k( id, scale, radius, contrast):
        r = SANSSphereModelKernel()
        r.id = id
        r.scale = scale
        r.radius = radius
        r.contrast = contrast
        return r

    records = [
        k( 'sansspheremodelkernel-0', 1.e-6, 60, 1),
        ]

    for r in records: db.insertRow( r )
    return


# version
__id__ = "$Id$"

# End of file 
