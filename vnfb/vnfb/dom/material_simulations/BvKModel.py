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


from dsaw.model.Inventory import Inventory as InvBase


from vnfb.dom.AtomicStructure import Structure
from BvKBond import BvKBond

class BvKModel(object):

    matter = Structure()
    short_description = ''
    bonds = []

    long_description = ''
    reference = ''

    class Inventory(InvBase):
        
        matter = InvBase.d.reference(name='matter', targettype=None, targettypes=[Structure], owned=0)
        short_description = InvBase.d.str(name='short_description', label='description')

        bonds = InvBase.d.referenceSet(name='bonds', targettype=BvKBond, owned=1)

        long_description = InvBase.d.str(name='long_description', label='details', max_length=2048)
        reference = InvBase.d.str(name='reference', max_length=1024)

        
        dbtablename = 'bvkmodels'




# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['properties', 'bonds']
BvKModel.customizeLubanObjectDrawer = customizeLubanObjectDrawer



# !!! needs update
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
        bvk( 'fccNi-000001', '', '09/26/2008', (PolyCrystal, 'polyxtalfccNi0'),
             "A bvk model for fcc Ni") 
        ]
    for b in bvks: db.insertRow( b )
    return


def initids():
    return [
        'fccNi-000001',
        ]


# version
__id__ = "$Id$"

# End of file 
