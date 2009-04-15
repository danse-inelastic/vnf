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




class Extension1:

    def onImage(self, image):
        return
    


from SlidableGallery import JSMill as SlidableGalleryMill
from Plot_2DMill import JSMill as Plot_2DMill
from ImagePlotMill import JSMill as ImagePlotMill
from SolidView3DMill import JSMill as SolidView3DMill
from AutoRefreshRenderer import JSMill as AutoRefreshRenderer
from TableMill import JSMill as TableMill
from TreeViewMill import JSMill as TreeViewMill
from UploaderMill import JSMill as UploaderMill
from DialogMill import JSMill as DialogMill
from JSsnippetMill import JSMill as JSsnippetMill

extensions = [
    Plot_2DMill,
    ImagePlotMill,
    SolidView3DMill,
    SlidableGalleryMill,
    AutoRefreshRenderer,
    TableMill,
    TreeViewMill,
    UploaderMill,
    DialogMill,
    JSsnippetMill,
    Extension1,
    ]


# version
__id__ = "$Id$"

# End of file 
