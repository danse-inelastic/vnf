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
        actor_name = actor
        actor = director.retrieveActor( actor_name )
        
        # what kind of haxor code is this if statement?!?!   Jiao?
        if actor is None:
            class _: pass
            actor = _(); actor.name = actor_name
        else:        
            director.configureComponent( actor )
            
        # these next few lines are extremely pythonic
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
