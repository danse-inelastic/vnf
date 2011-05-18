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

    def _createOverview(self, tabs, id=None):
        #
        director = self.director
        
        #
        domaccess = director.retrieveDOMAccessor('computation')
        #     
        computation = domaccess.getComputationRecord('arcsiqeresolutioncomputations', id)
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


    _tabnames = [
        ]
    def _tabname2histograms(self, name):
        histids = panels[name]
        p = lambda id: 'out/%s.h5' % id
        return map(p, histids)
    


panels = {
    'Beam monitors':
        ('mon1-itof-focused',
         'mon2-itof-focused'),
    }


# version
__id__ = "$Id$"

# End of file 
