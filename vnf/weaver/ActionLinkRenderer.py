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



class ActionLinkRenderer:


    def __init__(self, cgihome):
        self.cgihome = cgihome
        from ActionHrefRenderer import ActionHrefRenderer
        self.hrefer = ActionHrefRenderer( cgihome )
        return


    def render(self, action):
        return action.identify(self)


    def on_(self, action):
        href = self.hrefer.render( action )
        label = action.label
        return _link( label, href)

    onActionRequireAuthentication = on_
    onAction = on_



def _link( label, href ):
    return '<a href="%s">%s</a>' % (href, label)
        


# version
__id__ = "$Id$"

# End of file 
