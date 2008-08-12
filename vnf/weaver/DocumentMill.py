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


from opal.weaver.DocumentMill import DocumentMill as base
from ActionLinkRenderer import ActionLinkRenderer


class DocumentMill(ActionLinkRenderer, base):

    def __init__(self, tagger, configurations):
        base.__init__(self, tagger)
        
        cgihome = configurations['cgihome']
        ActionLinkRenderer.__init__(self, cgihome)

        from TreeViewMill import TreeViewMill
        self.treeviewmill = TreeViewMill(configurations)
        
        from AccordionMill import AccordionMill
        self.accordionMill = AccordionMill(configurations)

        self.configurations = configurations
        return


    def onTreeView(self, treeview):
        return self.treeviewmill.render( treeview )


    def onAccordion(self, accordion):
        return self.accordionMill.render( accordion )


    def onImage(self, image):
        path = os.path.join( self._imageStore(), image.path )
        return [ '<img src="%s" />' % path ]
    

    def onSlidableGallery(self, gallery):
        configurations = self.configurations
        home = configurations['home']
        cgihome = configurations['cgihome']
        
        csscode = []
        csscode.append( '<link rel="stylesheet" type="text/css" href="%s/css/slidableGallery/slidableGallery.css" />' % home )

        htmlcode = []
        gid = id(gallery)
        htmlcode.append( '<div id="%s">' % gid )
        htmlcode.append( '<ul>' )

        for image, action in gallery.images:
            href = action_href( action, cgihome )
            image = os.path.join( self._imageStore(), image )
            htmlcode.append(
                '<li><a href="%s"><img src="%s" /></a></li>' % (href,image)
                )
            continue
        
        htmlcode.append( '</ul>' )
        htmlcode.append( '</div>' )

        includes = []
        javascriptpath = configurations['javascriptpath']
        includes.append( '<SCRIPT src="%s/jquery/jquery.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/ui/ui.core.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/ui/ui.slider.js"></SCRIPT>' % javascriptpath )
        includes.append( '<SCRIPT src="%s/jquery/slidableGallery.js"></SCRIPT>' % javascriptpath )

        jscode = []
        jscode.append( '$(document).ready(function() {')
        jscode.append( '$("#%s").slidableGallery( [] );' % gid )
        jscode.append( '});' );
        
        codes = csscode + includes + ['<script>']  + jscode + ['</script>'] + htmlcode
        return codes


    def _imageStore(self):
        home = self.configurations['home']
        return os.path.join( home, 'images' )

    pass # end of DocumentMill


import os
from vnf.weaver import action_href


# version
__id__ = "$Id$"

# End of file 
