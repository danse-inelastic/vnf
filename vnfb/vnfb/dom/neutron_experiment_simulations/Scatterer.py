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


# meaning "Scatterer" can be used as a sample in an experiment simulation
from neutron_components.SampleBase import SampleBase, TableBase


class Scatterer(SampleBase):

    matter = None
    shape = None

    kernels = []
    
    scatterername = '' # name of this scatterer in the sample assembly
    position = [0.,0.,0.]
    orientation = [[1.,0.,0.],
                   [0.,1.,0.],
                   [0.,0.,1.],]
    referencename = '' # name of the scatterer in the sample assembly that this scatterer uses as reference

    short_description = ''

    pass # end of Scatterer


from _ import AtomicStructure, \
     geometry, AbstractShape, \
     scattering_kernels, AbstractScatteringKernel
shapetypes = geometry.getShapeTypes()
sktypes = scattering_kernels.getKernelTypes()

from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    matter = InvBase.d.reference(
        name = 'matter', targettype=AtomicStructure, owned=0)
    
    shape = InvBase.d.reference(
        name = 'shape',
        targettype=AbstractShape, targettypes=shapetypes, owned=1)

    kernels = InvBase.d.referenceSet(
        name='kernels',
        targettype=AbstractScatteringKernel, targettypes=sktypes, owned=1)

    
    scatterername = InvBase.d.str(name='scatterername')
    position = InvBase.d.array(name='position', elementtype='float', shape=3)
    orientation = InvBase.d.array(name='orientation', elementtype='float', shape=(3,3))
    referencename = InvBase.d.str(name='referencename')

    short_description = InvBase.d.str(name='short_description')

    dbtablename = 'scatterers'

    pass # end of Inventory

Scatterer.Inventory = Inventory
del Inventory


from _ import o2t
ScattererTable = o2t(Scatterer, {'subclassFrom': TableBase})



# obsolete
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
