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


from Actor import Actor, action_link, action, actionRequireAuthentication
from vnf.weaver import action_href

class Sample(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage( 'sample' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of samples')
        document.description = ''
        document.byline = 'byline'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        where = "creator='%s' or creator='vnf'" % director.sentry.username
        samples = clerk.indexSamples(where=where).values()
        scatterers = clerk.indexScatterers(where=where).values()
        all = samples+scatterers

        from vnf.utils.uniquelist import uniquelist
        from vnf.dom.hash import hash
        samples = uniquelist(all, idfun=lambda sample: hash(sample, clerk.db))

        table = director.retrieveComponent(
            'samples', factory="table", args=[samples, director],
            vault=['tables']).table
        document.contents.append(table)

        p = document.paragraph()
        p.text = [
            action_link(
                actionRequireAuthentication(
                    'sampleInput', 
                    director.sentry,
                    label = 'Add a new sample',
                    routine = 'default'   
                    ),
                director.cgihome,
                ),
            ]

        return page  


    def __init__(self, name=None):
        if name is None:
            name = "sample"
        super(Sample, self).__init__(name)
        return


# version
__id__ = "$Id$"

# End of file 
