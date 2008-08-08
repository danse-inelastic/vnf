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


from OwnedObject import OwnedObject


class SampleAssembly(OwnedObject):

    name = "sampleassemblies"
    
    import pyre.db

    status = pyre.db.varchar( name = 'status', default = 'new', length = 16 )

    import vnf.dom
    scatterers = vnf.dom.referenceSet( name = 'scatterers' )

    pass # end of SampleAssembly


def inittable(db):
    def sa( id, short_description, status, scatterers ):
        r = SampleAssembly()
        r.id = id
        r.short_description = short_description
        r.status = status
        for scatterer in scatterers:
            r.scatterers.add( scatterer, db )
            continue
        return r

    from Scatterer import Scatterer
    records = [
        sa( 'polyxtal-fccNi-plate-sampleassembly-0',
            'Sample only. Polycrystalline fcc Ni plate',
            'created',
            [ (Scatterer, 'polyxtal-fccNi-scatterer-0'),
              ],
            ),
        ]

    for r in records: db.insertRow( r )
    return



# version
__id__ = "$Id$"

# End of file 
