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
class Cylinder(base):

    name = 'cylinders'

    import dsaw.db

    height = dsaw.db.real( name = 'height', default = 0.1 )
    innerradius = dsaw.db.real( name = 'innerradius', default = 0.0 )
    outerradius = dsaw.db.real( name = 'outerradius', default = 0.002 )


def inittable(db):
    from idgenerator import generator
    def cylinder( id, height, innerradius, outerradius ):
        b = Cylinder()
        b.id = id
        b.height = height
        b.innerradius = innerradius
        b.outerradius = outerradius
        return b
    
    cylinders = [
        cylinder( 'cylinder0', 0.1, 0.0, 0.002 ),
        ]
    for c in cylinders: db.insertRow( c )
    return


def initids():
    return [
        'cylinder0',
        ]

# version
__id__ = "$Id$"

# End of file 
