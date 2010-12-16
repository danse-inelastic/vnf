# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2010  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from luban.components.AuthorizedActor import AuthorizedActor as base
from luban.content import select, alert, load
import luban.content as lc


class AuthorizedActor(base):

    pass # Actor


def portal(func, title, portlet=None):
    '''create a routine that can behave as a portal, which means
    that when a user login, he can directly see the visual created
    by "func".

    The way it is done is by using property
    "post_authorization_action" of the "login" actor.

    See actor "material_simulations/phonon_calculators/bvk",
        routine "P_editModel" 
    for an example.
    '''

    portlet = portlet or 'my-atomicstructures'
    
    def _(self, director):
        # target frame to change
        body_frame          = select(id='body-frame')
        # new body skeleton
        body_skeleton       = director.retrieveVisual(
            'body-skeleton', context='atomicstructure', director=director)
        main_display_area   = body_skeleton.find(id='main-display-area')
        # put stuff into the main display area
        doc = func(self, director)
        main_display_area.add(doc)
        
        # set page title
        setpagetitle = select(id='').setAttr(title=title)
        
        # help window
        helpwindow = director.redirect(
            actor='help', routine='createHelpWindow',
            nextpagetoshow = 'UserGuide-atomicstructures',
            include_credential=False)
        addhelpwindow = select(id='').append(helpwindow)

        # news ticker
        newsticker = director.redirect(
            actor='news', routine = 'createTicker',
            include_credential = False)
        addnewsticker = select(id='header-news-container').append(newsticker)
        
        # logout link
        logout = load(actor='logout')
        link = lc.link(label='logout', onclick=logout)
        addlogout = select(id='header-userinfo').append(link)

        # show dock
        showdock = select(id='dock').show()
        
        #
        return [
            setpagetitle,
            showdock,
            body_frame.replaceContent(body_skeleton),
            addhelpwindow,
            addnewsticker,
            addlogout,
            ]

    return _

# version
__id__ = "$Id$"

# End of file 
