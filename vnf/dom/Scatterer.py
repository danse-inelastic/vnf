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

from DbObject import DbObject as base
class Scatterer(base):

    name = 'scatterers'

    import pyre.db

    matter = pyre.db.versatileReference( name = 'matter', tableRegistry = tableRegistry)
    shape = pyre.db.versatileReference( name = 'shape', tableRegistry = tableRegistry)

    import vnf.dom
    kernels = vnf.dom.referenceSet( name = 'kernels' )
    
    pass # end of Scatterer


def inittable(db):
    def s( id, matter, shape, kernels ):
        r = Scatterer()
        r.id = id
        r.matter = matter
        r.shape = shape
        for kernel in kernels: r.kernels.add( kernel, db )
        return r

    from PolyCrystal import PolyCrystal
    from Block import Block
    from PolyXtalCoherentPhononScatteringKernel import PolyXtalCoherentPhononScatteringKernel
    
    records = [
        s( 'polyxtal-fccNi-scatterer-0',
           (PolyCrystal, 'polyxtalfccNi0'),
           (Block, 'plate0'),
           [ (PolyXtalCoherentPhononScatteringKernel,
              'polyxtalcoherentphononscatteringkernel-fccNi-0'),
             ],
           )
        ]
    
    for r in records: db.insertRow( r )
    return


# version
__id__ = "$Id$"

# End of file 
