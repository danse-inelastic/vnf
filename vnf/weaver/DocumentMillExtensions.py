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


class Extension1:

    def onImage(self, image):
        path = os.path.join( self._imageStore(), image.path )
        return [ '<img src="%s" />' % path ]
    

    def _imageStore(self):
        home = self.configurations['home']
        return os.path.join( home, 'images' )


import os



from ActionLinkRenderer import ActionLinkRenderer
from Plot_2DMill import Plot_2DMill
from ImagePlotMill import ImagePlotMill
from SolidView3DMill import SolidView3DMill
from AutoRefreshRenderer import AutoRefreshRenderer
from SlidableGallery import HtmlMill as SlidableGalleryMill
from TableMill import TableMill
from TreeViewMill import TreeViewMill

extensions = [
    ActionLinkRenderer,
    Plot_2DMill,
    ImagePlotMill,
    SolidView3DMill,
    SlidableGalleryMill,
    AutoRefreshRenderer,
    TableMill,
    TreeViewMill,
    Extension1,
    ]


# version
__id__ = "$Id$"

# End of file 
