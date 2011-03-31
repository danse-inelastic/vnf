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
class Cylinder(base):

    height = 0.1
    innerradius = 0.0
    outerradius = 0.002

    # end of Cylinder
    

    
from dsaw.model.Inventory import Inventory as InvBase
class Inventory(InvBase):

    dbtablename = 'cylinders'

    height = InvBase.d.float( name = 'height', default = 0.1 )
    height.tip = 'height. unit: meter'

    innerradius = InvBase.d.float( name = 'innerradius', default = 0.0 )
    innerradius.tip = 'innerradius. unit: meter'

    outerradius = InvBase.d.float( name = 'outerradius', default = 0.002 )
    outerradius.tip = 'outerradius. unit: meter'



Cylinder.Inventory = Inventory
del Inventory


from _ import o2t
CylinderTable = o2t(Cylinder)


# obsolete
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
