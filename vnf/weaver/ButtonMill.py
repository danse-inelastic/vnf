#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2009  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class HtmlMill:

    def onButton(self, button):
        configurations = self.configurations
        home = configurations['home']

        stylesheets = ['button.css']
        csscode = []
        for stylesheet in stylesheets:
            csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/%s" />' % (
                home, stylesheet) )
            continue

        htmlcode = []
        htmlcode.append( '<div><table><tr>' )
        htmlcode.append( '<td id="%s" class="button">' % button.id )
        htmlcode.append( button.label)
        htmlcode.append( '</td>' )
        htmlcode.append( '</tr></table></div>' )

        return csscode + htmlcode



class JSMill:

    def onButton(self, button):
        return
        

# version
__id__ = "$Id$"

# End of file 
