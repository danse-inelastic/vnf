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


class Action:

    def __init__(self, actor,
                 label = '', routine = None, arguments = {}, **kwds ):
        self.actor = actor
        self.label = label
        self.routine = routine
        kwds.update( arguments )
        self.arguments = kwds
        return

    def identify(self, visitor):
        return visitor.onAction( self )

    pass # end of Action




# version
__id__ = "$Id$"

# End of file 
