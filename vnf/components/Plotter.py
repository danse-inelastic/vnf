#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, actionRequireAuthentication, AuthenticationError


class Plotter(Actor):

    class Inventory(Actor.Inventory):

        import pyre.inventory

        pass # end of Inventory


    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'plotter' )
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        username = director.sentry.username
        userrecord = director.clerk.getUser( username )
        fullname = userrecord.fullname
        title = 'Welcome to the Virtual Neutron Facility, %s!' % (
            fullname,),
        document = main.document(title=title)
        
        p = form.paragraph()
        p.text = ['''<a href="/java/cod2.jnlp">Future Image of COD</a>''']  
        
        p = document.paragraph()
        action = actionRequireAuthentication(
            actor = 'neutronexperiment', sentry = director.sentry,
            label = 'run virtual neutron experiments', routine = 'default',
            )
        link = action_link( action, director.cgihome )
        p.text = [
            'In this web service facility, you can %s. ' % link,
            'In a virtual neutron experiment, ',
            'virtual neutrons are generated from a virtual neutron moderator,',
            'guided by virtual neutron guides,',
            'scattered by a virtual sample and sample environment,',
            'and intercepted by detectors.',
            ]



        return page


    def __init__(self, name=None):
        if name is None:
            name = "greet"
        super(Greeter, self).__init__(name)
        return


    pass # end of Greeter


# version
__id__ = "$Id$"

# End of file 
