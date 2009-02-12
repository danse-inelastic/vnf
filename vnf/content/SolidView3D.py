#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class SolidView3D:

    '''3d view of solid
    '''

    def __init__(self, solid, height=600, width=600):
        self.solid = solid
        self.width = width
        self.height = height
        return

    def identify(self, visitor):
        return visitor.onSolidView3D(self)


# version
__id__ = "$Id$"

# End of file 
