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


from WebApplication import WebApplication as base

class WebApplication(base):

    def main(self, *args, **kwds):
        actor = self.retrieveActor('in-maintenance-alert')
        self.configureComponent(actor)
        page = actor.default(self)
        return self.render(page)
        


# version
__id__ = "$Id$"

# End of file 
