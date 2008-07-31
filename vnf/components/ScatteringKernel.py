#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                     California Institute of Technology
#                       (C) 2007  All Rights Reserved
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from Actor import Actor, action_link, action, actionRequireAuthentication


class ScatteringKernel(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage('scatteringKernel')
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of scattering kernels')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        scatteringKernels = clerk.indexScatteringKernels().values()
        scatteringKernels = [ clerk.getHierarchy(scatteringKernel) for scatteringKernel in scatteringKernels]
            
        p = document.paragraph()
        numScatteringKernels = len(scatteringKernels)
        columns = ['id', 'reference', 'short_description', 'type', 'creator', 'date' ]
        columnTitles = ['Short description', 'Type of scattering kernel', 'Creator', 'Date of creation']

        from PyHtmlTable import PyHtmlTable
        t = PyHtmlTable(numScatteringKernels, len(columnTitles), {'width':'400','border':2})#,'bgcolor':'white'})
        for colNum, col in enumerate(columnTitles):
            t.setc(0,colNum,col)
            
        for row, sk in enumerate(scatteringKernels):
            for colNum, colName in enumerate( columns[2:] ):           
                value = sk.getColumnValue(colName)
                if colName == 'short_description':
                    link = action_link(
                        actionRequireAuthentication(
                        'scatteringKernel',
                        director.sentry,
                        label = value,
                        routine = 'show',
                        id = sk.id,
                        ),  director.cgihome
                        )
                    value = link
                t.setc(row+1,colNum,value)
        p.text = [t.return_html()]
        
        p = document.paragraph()
        p.text = [action_link(
        actionRequireAuthentication(
        'scatteringKernelInput', director.sentry,
        label = 'Add a new scattering kernel'),  director.cgihome
        ),
        '<br>']
        return page          

# this method should be altered so it loads all the values into the form fields
# and basically gives the user complete editing power
    def show(self, director):
        page = director.retrieveSecurePage( 'scatteringKernel' )
        
        id = self.inventory.id
        record = director.clerk.getJob( id )

        main = page._body._content._main
        document = main.document( title = '%s' % (record.description,) )

        props = record.getColumnNames()
        lines = ['%s=%s' % (prop, getattr(record, prop) ) for prop in props]
        for line in lines:
            p = document.paragraph()
            p.text = [line]
            continue
        return page


    def __init__(self, name=None):
        if name is None:
            name = "scatteringKernel"
        super(ScatteringKernel, self).__init__(name)
        return








# version
__id__ = "$Id$"

# End of file 
