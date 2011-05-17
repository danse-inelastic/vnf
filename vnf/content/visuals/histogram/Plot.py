# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                 Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
factory for a plot of a histogram

this is different from "View", which usually contains 
display of meta data as well ass plot. "View" should
reuse this factory here to generate plot.
"""


import luban.content


class Factory(object):

    def __init__(self, director=None):
        self.director = director
        return

        
    def build(self, histogram=None):
        """
        inputs:
        
        * histogram: the histogram instance
        """

        #
        director = self.director
        
        #
        dim = histogram.dimension()

        if dim==1:
            vis = luban.content.document(id='histogram-plot-container')
            p = luban.content.plot2d(); vis.add(p)
            xaxis = histogram.axes()[0]
            x = list(xaxis.binCenters())
            y = list(histogram.I)
            p.curve(x=x,y=y)
            notes = luban.content.rstdoc(id='histogram-plot-notes'); vis.add(notes)
            notes.text = [
                '* x axis unit: %s' % xaxis.unit(),
                ]
        elif dim == 2:
            vis = director.retrieveVisual(
                'histogram/imageplot',
                histogram=histogram,
                director=director,
                )
        else:
            raise NotImplementedError

        return vis

    
# version
__id__ = "$Id$"

# End of file 
