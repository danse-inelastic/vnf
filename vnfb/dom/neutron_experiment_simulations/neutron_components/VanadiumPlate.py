# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from SampleBase import SampleBase as base, TableBase
class VanadiumPlate(base):
    
    abstract = False

    width = 0.05; height = 0.10; thickness = 0.002

    target_radius = 0
    target_position = (0,0,0)


    def customizeLubanObjectDrawer(self, drawer):
        drawer.mold.sequence = [
            'componentname', 'short_description',
            'referencename', 'position', 'orientation',
            'width', 'height', 'thickness',
            'target_radius', 'target_position',
            ]

    pass


InvBase=base.Inventory
class Inventory(InvBase):

    # dimensions (unit: meter)
    width = InvBase.d.float(name='width', default=0.05, validator=InvBase.v.positive)
    height = InvBase.d.float(name='height', default=0.10, validator=InvBase.v.positive)
    thickness = InvBase.d.float(name='thickness', default=0.002, validator=InvBase.v.positive)

    # target definition
    target_radius = InvBase.d.float(name='target_radius', default=0)
    target_radius.tip = 'radius of disk containg target. use 0 for full space'
    
    target_position = InvBase.d.array(name='target_position', elementtype='float', default=(0,0,0))
    
    dbtablename = 'vanadiumplates'

    
VanadiumPlate.Inventory = Inventory
del Inventory


from _ import o2t
VanadiumPlateTable = o2t(VanadiumPlate, {'subclassFrom': TableBase})



# obsolete ...
def inittable(db):
    Table = VanadiumPlate
    def new(id, short_description, width, height, thickness, target_radius, target_position):
        r = Table()
        r.id = id
        r.short_description = short_description
        r.width = width
        r.height = height
        r.thickness = thickness
        r.target_radius = target_radius
        r.target_position = target_position
        return r
    records = [
        new('vanadiumplate-000001', 'Vanadium plate',
            0.05, 0.10, 0.002, 0, (0,0,0)),
        ]
    for r in records: db.insertRow( r )
    return


def initids():
    return [
        'vanadiumplate-000001',
        ]


# version
__id__ = "$Id$"

# End of file 
