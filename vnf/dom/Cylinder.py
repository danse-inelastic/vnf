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


from DbObject import DbObject
class Cylinder(DbObject):

    name = 'cylinders'

    import pyre.db

    height = pyre.db.real( name = 'height', default = 0.1 )
    innerradius = pyre.db.real( name = 'innerradius', default = 0.0 )
    outerradius = pyre.db.real( name = 'outerradius', default = 0.002 )


# version
__id__ = "$Id$"

# End of file 
