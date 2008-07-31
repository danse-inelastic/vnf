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


class SKResults(Actor):

    def default(self, director):
        try:
            page = director.retrieveSecurePage( 'sKResults' )
        except AuthenticationError, error:
            return error.page
        main = page._body._content._main

        # populate the main column
        document = main.document(title='Scattering Kernel Results')

        p = document.paragraph()
        p.text = ['Here are the results of running the simulation on ...']        
        p = document.paragraph()
        p.text = ['<a href="/java/SqePlot.jnlp">Plot of S(Q,E)</a><br>']
        return page

    def __init__(self, name=None):
        if name is None:
            name = "sKResults"
        super(SKResults, self).__init__(name)
        return


# version
__id__ = "$Id$"

# End of file 
