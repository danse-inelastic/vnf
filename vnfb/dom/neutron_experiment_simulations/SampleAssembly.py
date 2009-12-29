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




class SampleAssembly(object):

    scatterers = []

    pass # end of SampleAssembly


from Scatterer import Scatterer


# db table
from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    scatterers = InvBase.d.referenceSet(
        name = 'scatterers', targettype=Scatterer, owned = 0)
    
    dbtablename = 'sampleassemblies'


SampleAssembly.Inventory = Inventory
del Inventory


# orm
from _ import o2t, OwnedObject
SampleAssemblyTable = o2t(SampleAssembly, {'subclassFrom': OwnedObject})



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
