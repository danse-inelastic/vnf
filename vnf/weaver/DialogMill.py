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

    def onDialog(self, dialog):
        configurations = self.configurations
        home = configurations['home']
        cgihome = configurations['cgihome']

        # css
        stylesheets = [
            'dialog.css',
            'jquery-ui/smoothness/ui.all.css',
            ]
        csscode = []
        for stylesheet in stylesheets:
            csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/%s" />' % (
                home, stylesheet) )
            continue

        # html
        htmlcode = []

        # render
        htmlcode += self.onDocument(dialog)
        
        return csscode + htmlcode



class JSMill:

    def onDialog(self, dialog):
        configurations = self.configurations
        cgihome = configurations['cgihome']

        includes = [
            'jquery/jquery.js',
            'jquery/ui/ui.core.js',
            'jquery/ui/ui.draggable.js',
            'jquery/ui/ui.resizable.js',
            'jquery/ui/ui.dialog.js',
            #'jquery/elementFactory.js',
            'jquery/dialog.js',
            ]
        self.include(scripts=includes)

        self.writemain( '$("#%s").dialog( {' % (dialog.id, ) )
        self.writemain( '  bgiframe: true,' )
        self.writemain( '  autoOpen: false,' )
        #self.writemain( '  height: 300,' )
        self.writemain( '  modal: true,' )
        self.writemain( '  buttons: {' )
        self.writemain( '  },')
        self.writemain( '  close: function () {' )
        self.writemain( '  } ')
        self.writemain( '});' )

        for item in dialog.contents:
            item.identify(self)
        return
        

# version
__id__ = "$Id$"

# End of file 
