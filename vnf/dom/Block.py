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


from Shape import Shape as base
class Block(base):

    name = 'blocks'

    import pyre.db

    width = pyre.db.real( name = 'width', default = 0.05 )
    height = pyre.db.real( name = 'height', default = 0.1 )
    thickness = pyre.db.real( name = 'thickness', default = 0.002 )
    
    pass # end of Block


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


# version
__id__ = "$Id$"

# End of file 
