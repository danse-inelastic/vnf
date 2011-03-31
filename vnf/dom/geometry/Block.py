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


from AbstractShape import AbstractShape as base
class Block(base):

    width = 0.05
    height = 0.1
    thickness = 0.002
    
    pass # end of Block



from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    dbtablename = 'blocks'

    width = InvBase.d.float( name = 'width', default = 0.05 )
    width.tip = 'width. unit: meter'
    
    height = InvBase.d.float( name = 'height', default = 0.1 )
    height.tip = 'height. unit: meter'

    thickness = InvBase.d.float( name = 'thickness', default = 0.002 )
    thickness.tip = 'thickness. unit: meter'
    

Block.Inventory = Inventory
del Inventory


from _ import o2t
BlockTable = o2t(Block)


# obsolete
def inittable(db):
    from idgenerator import generator
    def block( id, width, height, thickness ):
        b = Block()
        b.id = id
        b.width = width
        b.height = height
        b.thickness = thickness
        return b
    
    blocks = [
        block( 'plate0', 0.05, 0.1, 0.002 ),
        ]
    for b in blocks: db.insertRow( b )
    return


def initids():
    return [
        'plate0',
        ]

# version
__id__ = "$Id$"

# End of file 
