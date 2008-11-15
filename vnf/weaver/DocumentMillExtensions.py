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


from ActionLinkRenderer import ActionLinkRenderer

class Extension1:

    def onTreeView(self, treeview):
        from TreeViewMill import TreeViewMill
        mill = TreeViewMill(self.configurations)
        return mill.render(treeview)


    def onTable(self, table):
        from TableMill import TableMill
        mill = TableMill(self.configurations)
        return mill.render(table)


    def onImage(self, image):
        path = os.path.join( self._imageStore(), image.path )
        return [ '<img src="%s" />' % path ]
    

    def _imageStore(self):
        home = self.configurations['home']
        return os.path.join( home, 'images' )


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



from vnf.weaver import action_href
import os


extensions = [
    ActionLinkRenderer,
    Extension1,
    ]


# version
__id__ = "$Id$"

# End of file 
