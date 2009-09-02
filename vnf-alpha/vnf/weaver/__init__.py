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



def action_link(action, cgihome):
    from ActionLinkRenderer import ActionLinkRenderer
    renderer = ActionLinkRenderer( cgihome )
    return renderer.render( action )[0]

def action_href(action, cgihome):
    from ActionHrefRenderer import ActionHrefRenderer
    renderer = ActionHrefRenderer( cgihome )
    return renderer.render( action )

def action_formfields( action, form ):
    from ActionMill_forForm import ActionMill_forForm
    renderer = ActionMill_forForm( form )
    return renderer.render( action )


def pageMill(configurations):
    from PageMill import PageMill
    return PageMill(configurations)


# version
__id__ = "$Id$"

# End of file 
