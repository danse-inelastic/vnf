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


def extend_weaver(weaver, configurations):
    weaver.bodyMill.structuralMill = structuralMill(
        weaver.bodyMill.tagger, configurations)
    return


def structuralMill(tagger, configuration):
    from StructuralMill import StructuralMill
    return StructuralMill(tagger, configuration)


# version
__id__ = "$Id$"

# End of file 
