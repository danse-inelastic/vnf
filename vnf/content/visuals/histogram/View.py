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
visual factory for a histogram
"""

import luban.content


class Factory(object):

    def __init__(self, director=None):
        self.director = director
        return

        
    def build(self, histogram=None, downloadaction=None):
        """build the visual
        
        inputs:

        * histogram: the histogram instance
        * downloadaction: action to download histogram
        """
        
        director = self.director

        dim = histogram.dimension()

        # title
        try:
            title = histogram.getAttribute('title')
        except KeyError:
            title = 'Histogram I(%s)' % (
                ','.join(['%s(%s)' % (axis.name(), axis.unit()) 
                          for axis in histogram.axes()]),
                )

        # container
        doc = luban.content.document(Class='container', title=title, collapsable=True)

        # plot
        from Plot import Factory
        plotfac = Factory(director=director)
        plot = plotfac.build(histogram=histogram)
        doc.add(plot)

        # download button
        downloader = luban.content.downloader(
            label = 'download data', 
            ondownload = downloadaction,
            )
        doc.add(downloader)

        return doc

    
# version
__id__ = "$Id$"

# End of file 
