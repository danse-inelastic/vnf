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


from Action import Action

class ActionRequireAuthentication( Action ):

    def __init__(self, actor, sentry, label = '', routine = None, target = None,
                 arguments = {}, **kwds ):
        Action.__init__(self, actor, label, routine, target, arguments, **kwds )
        self.sentry = sentry
        return

    def identify(self, visitor):
        return visitor.onActionRequireAuthentication(self)

    pass # end of ActionRequireAuthentication



# version
__id__ = "$Id$"

# End of file 
