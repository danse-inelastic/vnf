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
            page = director.retrieveSecurePage('plotter')
        except AuthenticationError, error:
            return error.page

        main = page._body._content._main

        # populate the main column
        username = director.sentry.username
        userrecord = director.clerk.getUser( username )
        fullname = userrecord.fullname
        title = 'Plotter',
        document = main.document(title=title)
        
        p = document.paragraph()
        p.text = ['Here is the applet:<br>',
                  '''<applet code="http://trueblue.caltech.edu/java/PlotterApplet.class" 
                  archive="http://trueblue.caltech.edu/java/visad.jar" width="600" height="600"></applet><br>''',
                  'Here is <a href="/java/sqeViewer3.jnlp">webstart</a><br>']#,
                  #'<a href="/java/PlotterAll.jnlp">Simple Plot</a>']  
        

        return page


    def __init__(self, name=None):
        if name is None:
            name = "plotter"
        super(Actor, self).__init__(name)
        return



# version
__id__ = "$Id$"

# End of file 
