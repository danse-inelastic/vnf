#!/usr/bin/env python
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2009  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from luban.content.Splitter import Splitter
from luban.content.Paragraph import Paragraph
from luban.content import load
from luban.content.Link import Link

# Stub at this point
class QEServer:

    def __init__(self, director):
        self._director  = director
        self._clerk     = director.clerk
 
    def getLink(self, id):      # simulation id
        server = None
        sim     = self._director.clerk.getQESimulations(id = id )
        if sim:
            server = self._director.clerk.getServers(id = sim.serverid )

        link = Paragraph(text="None")

        if server:
            link = Link(label=server.address, Class="action-link",
                        onclick=load(actor      = "server",
                                     routine    = "view",
                                     id         = server.id)
                        )

        return link


if __name__ == "__main__":
    pass


__date__ = "$Nov 11, 2009 1:21:52 PM$"


#    def getServer(self, id):      # simulation id
#        settings    = self._clerk.getQEConfigurations(where="simulationid='%s' AND type='%s'" % (id, self._type))
#        servername  = self._serverName(settings)
#
#        if servername   != '':  
#            text    = Link(label=servername, Class="action-link",
#                           onclick=load(actor="materialsimulation"))
##                           routine="view",
##                           sname=servername))
#        else:
#            text    = Paragraph(text="None")
#
#        return text
#
#    def _serverName(self, settings):
#        """Get the server name"""
#        # settings is list of Configuration tables
#        if len(settings) == 0:
#            return ''
#
#        import ConfigParser
#        import StringIO
#
#        if settings[0]:
#            # check if settings[0] isinstanceof Configuration
#            config  = settings[0].text  
#
#            """
#            Example of config:
#            config  = "
#            [server]
#            server-name = foxtrot.danse.us
#            "
#            """
#            if config:  # Implies that it has sections already
#                fp  = StringIO.StringIO(config)
#                parser  = ConfigParser.ConfigParser()
#                parser.readfp(fp)
#                name    = parser.get("server", "server-name")
#
#                if self._isServerName(name):
#                    return name
#
#        return ''
#                
#    def _isServerName(self, name):
#        return True
    
#        if name == '':
#            return False
#
#        if self._director:
#            servers  = self._clerk.getServers()
#            for s in servers:
#                """Check if the server name is available in the server names """
#                if name == s.sname:
#                    return True
#
#        return False
