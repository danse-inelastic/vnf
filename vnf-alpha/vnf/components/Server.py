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
from wording import plural, present_be


class Server(Actor):

    class Inventory(Actor.Inventory):

        import time
        import pyre.inventory

        id = pyre.inventory.str("id", default=None)
        id.meta['tip'] = "the unique identifier for a given search"
        
        page = pyre.inventory.str('page', default='empty')

    def default(self, director):
        return self.listall( director )

    def listall(self, director):
        page = director.retrievePage( 'server' )
        
        main = page._body._content._main
        
        # populate the main column
        document = main.document(title='List of servers')
        document.description = ''
        document.byline = 'byline?'

        # retrieve id:record dictionary from db
        clerk = director.clerk
        servers = clerk.getServers()
        columnNames=['Name','Location','Group Access','Working Directory','Scheduler']
        numColumns=len(columnNames)
        
        serverValues=[]
        for server in servers:
            serverValues.append(server.getValues())
            
        p = document.paragraph()
        numServers = len(servers)
        numColumns=servers[0].getNumColumns()

        from PyHtmlTable import PyHtmlTable
        t=PyHtmlTable(numServers,numColumns, {'width':'400','border':2,'bgcolor':'white'})
        for row in range(numServers):
            colNum=0
            for name in servers[row].getColumnNames():
                t.setc(row,colNum,servers[row].getColumnValue(name))
                colNum+=1
        p.text = [t.return_html()]
        
        return page  


    def __init__(self, name=None):
        if name is None:
            name = "server"
        super(Server, self).__init__(name)
        return

# version
__id__ = "$Id$"

# End of file 
