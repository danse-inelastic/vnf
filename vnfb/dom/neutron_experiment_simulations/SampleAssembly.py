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


from neutron_components.SampleBase import SampleBase, TableBase

class SampleAssembly(SampleBase):

    scatterers = []

    position = [0.,0.,0.]
    orientation = [[1.,0.,0.],
                   [0.,1.,0.],
                   [0.,0.,1.],]

    pass # end of SampleAssembly


from Scatterer import Scatterer


# Inventory for orm
class Inventory(SampleBase.Inventory):
    
    scatterers = SampleBase.Inventory.d.referenceSet(
        name = 'scatterers', targettype=Scatterer, owned = 1)
        
    dbtablename = 'sampleassemblies'


SampleAssembly.Inventory = Inventory
del Inventory


# orm
from _ import o2t
SampleAssemblyTable = o2t(SampleAssembly, {'subclassFrom': TableBase})



# obsolete
# status = dsaw.db.varchar( name = 'status', default = 'new', length = 16 )
# ???
def inittable(db):
    def sa( id, short_description, status, scatterers ):
        r = SampleAssembly()
        r.id = id
        r.short_description = short_description
        r.status = status
        for name, scatterer in scatterers:
            r.scatterers.add( scatterer, db, name = name )
            continue
        return r

    from Scatterer import Scatterer
    records = [
        sa( 'polyxtal-fccNi-plate-sampleassembly-0',
            'Sample only. Polycrystalline fcc Ni plate',
            'created',
            [ ( 'sample', (Scatterer, 'polyxtal-fccNi-scatterer-0') ),
              ],
            ),
        ]

    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'polyxtal-fccNi-plate-sampleassembly-0',
        ]


# version
__id__ = "$Id$"

# End of file 
