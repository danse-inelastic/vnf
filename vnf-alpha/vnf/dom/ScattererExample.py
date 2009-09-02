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



from Scatterer import Scatterer

from DbObject import DbObject as base
class ScattererExample(base):

    # Examples of scatterers. Records of this table will serve
    # as templates and user can start from these templates and build
    # scatterers by modifying its parameters.

    name = 'scattererexampless'

    import dsaw.db

    scatterer = dsaw.db.reference( name = 'scatterer', table = Scatterer)

    pass # end of Scatterer


def inittable(db):
    def s( id, scatterer):
        r = ScattererExample()
        r.id = id
        r.scatterer = scatterer
        return r

    records = [
        s( 'polyxtal-fccNi-scatterer: example 0',
           'polyxtal-fccNi-scatterer-0',
           ),
        
        s( 'sans-sphere-model-scatterer: example 1',
           'sans-sphere-model-scatterer-0',
           ),
        ]
    
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'polyxtal-fccNi-scatterer: example 0',
        'sans-sphere-model-scatterer: example 1',
        ]

# version
__id__ = "$Id$"

# End of file 
