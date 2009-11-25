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


class SimServer:

    def __init__(self, director):
        self._director  = director
        self._clerk     = director.clerk
        self._type      = "settings"

    def getServer(self, id):      # simulation id
        settings    = self._clerk.getConfigurations(where="simulationId='%s' AND type='%s'" % (id, self._type))
        servername  = self._serverName(settings)

        if servername   != '':  
            text    = Link(label=servername, Class="action-link",
                           onclick=load(actor="server-view",
                           routine="link",
                           sname=servername))
        else:
            text    = Paragraph(text="None")

        return text

    def _serverName(self, settings):
        """Get the server name"""
        # settings is list of Configuration tables
        if len(settings) == 0:
            return ''

        import ConfigParser
        import StringIO

        if settings[0]:
            # check if settings[0] isinstanceof Configuration
            config  = settings[0].text  

        #Example of config:
        #config  = """
        #[server]
        #server-name = foxtrot.danse.us
        #"""
            if config:  # Implies that it has sections already
                fp  = StringIO.StringIO(config)
                parser  = ConfigParser.ConfigParser()
                parser.readfp(fp)
                name    = parser.get("server", "server-name")

                if self._isServerName(name):
                    return name

        return ''
                
    def _isServerName(self, name):
        if name == '':
            return False

        if self._director:
            servers  = self._clerk.getServers()
            for s in servers:
                """Check if the server name is available in the server names """
                if name == s.sname:
                    return True

        return False

        
#        s   = settings[0]
#        if s:
#            config  = s.text
            
        



    def _label(self, settings):
        """Returns filename"""
        if settings:
            return settings[0].filename

        return "Add"


    def _getActor(self, settings):
        """Returns proper actor depending if 'input' exists"""
        if settings:   # View
            return "espresso/settings-view"

        return "espresso/settings-add" # Create New




if __name__ == "__main__":
    params   = SimServer(None)
    #params.serverIsSet(None)


__date__ = "$Nov 11, 2009 1:21:52 PM$"


