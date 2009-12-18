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


# activate customized orm in vnf for atomic structure
import vnfb.dom.AtomicStructure


# deactivate the warning from importing bvk
import journal
journal.warning('UserWarning').deactivate()
import bvk
#
journal.warning('UserWarning').activate()



from bvk.orm.BvKModel import BvKModel


# view
def customizeLubanObjectDrawer(self, drawer):
    drawer.sequence = ['properties', 'bonds']
    drawer.readonly_view_sequence = ['matter', 'properties', 'bonds']
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
