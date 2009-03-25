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

        return csscode + htmlcode



class JSMill:

    def onSlidableGallery(self, gallery):
        if len(gallery.images) < 8:
            return
        else:
            includes = [
                'jquery/jquery.js',
                'jquery/ui/ui.core.js',
                'jquery/ui/ui.slider.js',
                'jquery/slidableGallery.js',
                ]
            self.include(scripts=includes)
            
            gid = id(gallery)
            self.writemain( '$("#%s").slidableGallery( [] );' % gid )
        
        return
        


from vnf.weaver import action_href
import os


# version
__id__ = "$Id$"

# End of file 
