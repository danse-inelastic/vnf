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

    def onTreeView(self, treeview):
        return


    def onImage(self, image):
        return
    


from SlidableGallery import JSMill as SlidableGalleryMill
from Plot_2DMill import JSMill as Plot_2DMill
from ImagePlotMill import JSMill as ImagePlotMill
from SolidView3DMill import JSMill as SolidView3DMill
from AutoRefreshRenderer import JSMill as AutoRefreshRenderer
from TableMill import JSMill as TableMill

extensions = [
    Plot_2DMill,
    ImagePlotMill,
    SolidView3DMill,
    SlidableGalleryMill,
    AutoRefreshRenderer,
    TableMill,
    Extension1,
    ]


# version
__id__ = "$Id$"

# End of file 
