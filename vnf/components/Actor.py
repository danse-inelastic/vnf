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


from vnf.applications.WebApplication import AuthenticationError
from vnf.content import action, actionRequireAuthentication
from vnf.weaver import action_link



from opal.components.Actor import Actor as base
class Actor(base):

    def redirect(self, director, actor, routine, *args, **kwds):
        actor = director.retrieveActor( actor )
        director.configureComponent( actor )
        director.inventory.actor = director.actor = actor
        
        director.inventory.routine = director.routine = routine

        try:
            handler = getattr(actor, routine)
        except:
            handler = None
            
        if handler is None:
            return director.retrievePage('nyi')
        
        return handler(director, *args, **kwds)
    

# version
__id__ = "$Id$"

# End of file 
