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
factory of histogram view for a computation
"""

import luban.content


from ...AbstractFactory import AbstractFactory
class Factory(AbstractFactory):
    
    
    def __init__(self, **kwds):
        """
        actor: the name of the actor for the computation. 
            it should handle "downloadHistogram"
        name, director: see AbstractFactory.__init__
        """
        super(Factory, self).__init__(**kwds)
        return
        

    def build(self, id=None, histogram_path=None):
        """
        id: id of the computation
        histogram_path: path of the histogram inside the directory for the computation
        """
        director = self.director
        domaccess = director.retrieveDOMAccessor('computation')

        def _gethist(path):
            from histogram.hdf import load
            from histogram.hdf.utils import getOnlyEntry
            computation = domaccess.getComputationRecord('arcsbeamconfigurations', id)
            dds = director.dds
            p = dds.abspath(computation, path)
            return load(p, getOnlyEntry(p))


        def _histview(histogram_path, histogram):
            from vnf.content.visuals.histogram.View import Factory
            vf = Factory(director=director)
            downloadaction = luban.content.load(
                actor = self.actor, 
                routine='downloadHistogram',
                id = id,
                histogram = histogram_path,
                )
            return vf.build(histogram=histogram, downloadaction=downloadaction)

        histogram = _gethist(histogram_path)
        return _histview(histogram_path, histogram)



# version
__id__ = "$Id$"

# End of file 
