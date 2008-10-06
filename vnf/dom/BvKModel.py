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


from registry import tableRegistry

from OwnedObject import OwnedObject as base

class BvKModel(base):

    name = 'bvkmodels'

    import pyre.db
    matter = pyre.db.versatileReference(name='matter', tableRegistry=tableRegistry)
    

def inittable(db):
    def bvk(id, creater, date, matter, short_description):
        b = BvKModel()
        b.id = id
        b.creater = creater
        b.date = date
        b.matter = matter
        b.short_description = short_description
        return b

    from PolyCrystal import PolyCrystal
    bvks = [
        bvk( 'fccNi', '', '09/26/2008', (PolyCrystal, 'polyxtalfccNi0'),
             "A bvk model for fcc Ni") 
        ]
    for b in bvks: db.insertRow( b )
    return



# version
__id__ = "$Id$"

# End of file 
