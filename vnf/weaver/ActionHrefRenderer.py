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


class ActionHrefRenderer:

    def __init__(self, cgihome):
        self.cgihome = cgihome
        return

    def render(self, action):
        return action.identify(self)

    def onAction(self, action):
        cgihome = self.cgihome
        arguments = {
            'actor': action.actor,
            }
        for k,v in action.arguments.iteritems():
            arguments[ '%s.%s' % (action.actor, k) ] = v
            continue

        routine = action.routine
        if routine: arguments['routine'] = routine
        
        return _address( cgihome, arguments )

    def onActionRequireAuthentication(self, action):
        cgihome = self.cgihome
        arguments = {
            'actor': action.actor,
            }
        for k,v in action.arguments.iteritems():
            arguments[ '%s.%s' % (action.actor, k) ] = v
            continue

        routine = action.routine
        if routine: arguments['routine'] = routine

        sentry = action.sentry
        username = sentry.username
        ticket = sentry.ticket
        arguments['sentry.username'] = username
        arguments['sentry.ticket'] = ticket
        
        return _address( cgihome, arguments ) 

def _address( cgihome, arguments ):
    return '%s?%s' % (
        cgihome,
        '&'.join( ['%s=%s' % (k,v) for k,v in arguments.iteritems() ] ),
        )

        


# version
__id__ = "$Id$"

# End of file 
