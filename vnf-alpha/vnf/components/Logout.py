#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, AuthenticationError


class Logout(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory



    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'login' )
        except AuthenticationError, err:
            return err.page            
        
        sentry = director.sentry
        ipa = sentry.ipa

        ipa.logout(sentry.username, sentry.ticket)

        actor = 'login'
        routine = 'default'
        return director.redirect(actor, routine)


    def __init__(self, name=None):
        if name is None:
            name = "logout"
        super(Logout, self).__init__(name)
        return


    pass # end of Logout


# version
__id__ = "$Id$"

# End of file 
