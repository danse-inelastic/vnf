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

class BvK(base):

    name = 'bvks'

    import pyre.db
    matter = pyre.db.versatileReference('matter', registry=tableRegistry)
    

def inittable(db):
    def bvk(id, creater, date, matter):
        b = BvK()
        b.id = id
        b.creater = creater
        b.date = date
        b.matter = matter
        return b

    from PolyCrystal import PolyCrystal
    bvks = [
        bvk( 'fccNi', '', '09/26/2008', (PolyCrystal, 'polyxtalfccNi0') ) 
        ]
    for b in bvks: db.insertRow( b )
    return



# version
__id__ = "$Id$"

# End of file 
