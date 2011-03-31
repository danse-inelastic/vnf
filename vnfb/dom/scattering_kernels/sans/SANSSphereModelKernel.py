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


from _ import AbstractScatteringKernel as base
class SANSSphereModelKernel(base):

    scale = 1e-6
    radius = 60.
    contrast = 1.0
    
    pass # end of SANSSphereModelKernel



from _ import AbstractScatteringKernelInventory as InvBase
class Inventory(InvBase):

    scale = InvBase.d.float( name = 'scale', default = 1e-6 )
    radius = InvBase.d.float( name = 'radius', default = 60.0 )
    contrast = InvBase.d.float( name = 'contrast', default = 1.0 )
    
    dbtablename = 'sansspheremodelkernels'
    
    pass # end of SANSSphereModelKernel


SANSSphereModelKernel.Inventory = Inventory
del Inventory
from _ import o2t, KernelTableBase
SANSSphereModelKernelTable = o2t(
    SANSSphereModelKernel,
    {'subclassFrom': KernelTableBase},
    )


# obsolete
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


def initids():
    return [
        'sansspheremodelkernel-0',
        ]


# version
__id__ = "$Id$"

# End of file 
