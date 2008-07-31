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
class Block(DbObject):

    name = 'blocks'

    import pyre.db

    width = pyre.db.real( name = 'width', default = 0.05 )
    height = pyre.db.real( name = 'height', default = 0.1 )
    thickness = pyre.db.real( name = 'thickness', default = 0.002 )
    
    pass # end of Block


# version
__id__ = "$Id$"

# End of file 
