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

import luban.content


from ResultsViewFactoryBase import Factory as base
class Factory(base):


    def build(self, id=None, **kwds):
        #
        director = self.director

        # 
        actor = kwds.get('actor') or self.actor
        
        #
        container = luban.content.document(id='%s-results-container' % self.name)
        tabs = luban.content.tabs(); container.add(tabs)

        # first tab
        tab = createOverview(tabs, director=director, id=id)

        # other tabs
        tabnames = [
            'Beam monitors',
            'Resolution at sample position',
            'Spatial distribution',
            'Divergence',
            ]
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


    def _createHistView(self, id=None, histogram_path=None):
        """create histogram view for a histogram
        
        id: id of the computation
        histogram_path: relative path of the histogram in the computation directory
        """
        from .HistogramView import Factory
        vf = Factory(
            actor=self.actor, 
            director=self.director, 
            name='beam-profile-histogram')
        return vf.build(id=id, histogram_path=histogram_path)

    
    def createPanel(self, id=None, panel=None, **kwds):
        histids = panels[panel]
        import collections
        q = collections.deque(histids)
        g = luban.content.grid()
        ncols = 1
        while q:
            row = g.row()
            for i in range(ncols):
                if not q: break
                hid = q.popleft()
                histogram_path = 'out/%s.h5' % hid
                cell = row.cell()
                histview = self._createHistView(id=id, histogram_path=histogram_path)
                cell.add(histview)
                continue
            continue
        container = luban.content.document()
        container.add(g)
        return container

        
panels = {
    'Beam monitors':
        ('mon1-itof-focused',
         'mon2-itof-focused'),
    'Resolution at sample position':
        ('itof',
         'ienergy'),
    'Spatial distribution':
        ('ix_y',),
    'Divergence':
        ('ix_divx', 'ix_divy',
         'iy_divx', 'iy_divy',),
    }


def createOverview(tabs, director, id):
    domaccess = director.retrieveDOMAccessor('computation')
    #     
    computation = domaccess.getComputationRecord('arcsbeamconfigurations', id)
    #
    dds = director.dds
    p = dds.abspath(computation, 'out/props.json')
    #
    d = eval(open(p).read())
    #
    doc = luban.content.rstdoc()
    doc.text = [
        'Computed properties',
        '-------------------',
        ]
    for k, v in d.iteritems():
        doc.text.append('* %s:%s' % (k,v))
        continue

    tab = tabs.tab('Overview')
    tab.add(doc)
    
    return tab


# version
__id__ = "$Id$"

# End of file 
