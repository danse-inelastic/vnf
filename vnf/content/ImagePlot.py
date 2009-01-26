#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                  Jiao Lin
#                     California Institute of Technology
#                       (C) 2008  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


class ImagePlot:

    '''image plot of z=f(x,y). z is shown as color.
    '''

    def __init__(self, data, options):
        self.data = data
        self.options = options
        return

    def identify(self, visitor):
        return visitor.onImagePlot(self)


# version
__id__ = "$Id$"

# End of file 
