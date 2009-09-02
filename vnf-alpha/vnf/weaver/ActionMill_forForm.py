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


class ActionMill_forForm:

    def __init__(self, form):
        self.form = form
        return

    def render(self, action):
        return action.identify(self)

    def onAction(self, action):
        arguments = {
            'actor': action.actor,
            }
        for k,v in action.arguments.iteritems():
            arguments[ '%s.%s' % (action.actor, k) ] = v
            continue

        routine = action.routine
        if routine: arguments['routine'] = routine

        form = self.form
        return _fields( form, arguments )

    def onActionRequireAuthentication(self, action):
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
        
        form = self.form
        return _fields( form, arguments ) 


def _fields( form, arguments ):
    for key in arguments:
        value = arguments.get(key)
        field = form.hidden( name = key, value = value )
        continue
    return         


# version
__id__ = "$Id$"

# End of file 
