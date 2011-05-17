# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                      (C) 2006-2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


"""
base class for visuals that displays results of a computation

"""


import luban.content


from ...AbstractFactory import AbstractFactory as base
class Factory(base):

    def build(self, id=None, **kwds):
        """ build results view for the given computation

        this default implementation presents a tabs-view

        tab #1: overview
        other tabs: each shows a bunch of histograms

        requirements:
        
        * self._createOverview method
        * self._tabnames: names of tabs other than the overview
        
        """
        
        #
        director = self.director

        # 
        actor = kwds.get('actor') or self.actor
        
        #
        container = luban.content.document(id='%s-results-container' % self.name)
        tabs = luban.content.tabs(); container.add(tabs)

        # first tab
        tab = self._createOverview(tabs, id=id)

        # other tabs
        tabnames = self._tabnames
        for tabname in tabnames:
            tab = tabs.tab(label=tabname)
            tab.onselect = luban.content.select(element=tab).replaceContent(
                luban.content.load(
                    actor=actor,
                    routine='loadVisual',
                    name = 'results_view',
                    method = "createPanel",
                    panel = tabname,
                    id = id,
                    )
                )
            continue
        return container


    def createPanel(self, id=None, panel=None, **kwds):
        """create result view panel (identified by its name) for the given computation 

        id: id of the computation
        panel: name of the panel

        this default implementation assumes that we have a map "tabname2histograms"
        that map a panel name to a list of histogram paths. and we will just
        create a panel containing a bunch of view of those histograms.

        requirements: 
          self._tabname2histograms: a method to map tab name to a list of histogram paths
        """
        histpaths = self._tabname2histograms(panel)
        import collections
        q = collections.deque(histpaths)
        g = luban.content.grid()
        ncols = 1
        while q:
            row = g.row()
            for i in range(ncols):
                if not q: break
                histogram_path = q.popleft()
                cell = row.cell()
                histview = self._createHistView(id=id, histogram_path=histogram_path)
                cell.add(histview)
                continue
            continue
        container = luban.content.document()
        container.add(g)
        return container

        
    def _createHistView(self, id=None, histogram_path=None):
        """create histogram view for a histogram
        
        id: id of the computation
        histogram_path: relative path of the histogram in the computation directory
        """
        from .HistogramView import Factory
        vf = Factory(
            actor=self.actor, 
            director=self.director, 
            name='%s-histogram' % self.name)
        return vf.build(id=id, histogram_path=histogram_path)


    def _createOverview(self, tabs, id=None):
        """in the tabs visual, create a tab for overview, and add content
        to that tab

        inputs:
        * tabs: tabs visual into which a new tab of overview will be added
        * id: id of the computation
        """
        raise NotImplementedError


    def _tabname2histograms(self, name):
        """map name of a tab to a list of histogram paths
        """
        raise NotImplementedError
    
    pass 


# version
__id__ = "$Id$"

# End of file 
