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


    def onAction(self, action):
        href = self.hrefer.render( action )
        label = action.label
        kwds = {}
        if action.target:
            kwds['target'] = action.target
        return [_link( label, href, **kwds)]

    onActionRequireAuthentication = onAction



def _link( label, href, **kwds ):
    arguments = kwds.items()
    arguments.append( ('href', href) )
    argsstr = ' '.join( ['%s="%s"' % (k,v) for k,v in arguments] )
    return '<a %s>%s</a>' % (argsstr, label)
        


# version
__id__ = "$Id$"

# End of file 
