# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2007  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from registry import tableRegistry

from OwnedObject import OwnedObject as base
class Scatterer(base):

    name = 'scatterers'

    import pyre.db

    matter = pyre.db.versatileReference( name = 'matter', tableRegistry = tableRegistry)
    shape = pyre.db.versatileReference( name = 'shape', tableRegistry = tableRegistry)

    import vnf.dom
    kernels = vnf.dom.referenceSet( name = 'kernels' )
    
    pass # end of Scatterer


def inittable(db):
    def s( id, creator, date, short_description, matter, shape, kernels ):
        r = Scatterer()
        r.id = id
        r.creator = creator
        r.date = date
        r.short_description = short_description
        r.matter = matter
        r.shape = shape
        for kernel in kernels: r.kernels.add( kernel, db )
        return r

    from PolyCrystal import PolyCrystal
    from Disordered import Disordered
    from Block import Block
    from Cylinder import Cylinder
    from ins.PolyXtalCoherentPhononScatteringKernel import PolyXtalCoherentPhononScatteringKernel
    from sans.SANSSphereModelKernel import SANSSphereModelKernel
    
    records = [
        s( 'polyxtal-fccNi-scatterer-0',
           'vnf',
           '2008/12/01',
           'fcc Ni plate',
           (PolyCrystal, 'polyxtalfccNi0'),
           (Block, 'plate0'),
           [ (PolyXtalCoherentPhononScatteringKernel,
              'polyxtalcoherentphononscatteringkernel-fccNi-0'),
             ],
           ),
        
        s( 'sans-sphere-model-scatterer-0',
           'vnf',
           '2008/12/01',
           'SANS sphere model sample',
           (Disordered, 'liquid0'),
           (Cylinder, 'cylinder0'),
           [ (SANSSphereModelKernel,
              'sansspheremodelkernel-0'),
             ],
           )
        ]
    
    for r in records: db.insertRow( r )
    return


def initids():
    'ids of records initialized by inittable()'
    return [
        'polyxtal-fccNi-scatterer-0',
        'sans-sphere-model-scatterer-0',
        ]


# version
__id__ = "$Id$"

# End of file 
