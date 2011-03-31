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

# XXX: Refactor

from luban.content.Splitter import Splitter
from luban.content.Paragraph import Paragraph
from luban.content import load, select
from luban.content.Link import Link

class QEServer:

    def __init__(self, director):
        self._director  = director
        self._clerk     = director.clerk
 
    def getLink(self, id):      # simulation id
        server = None
        link = "None"

        settings    = self._director.clerk.getQESettings(where="simulationid='%s'" % id )
        if not settings:# or not settings[0]:
            return link

        setting     = settings[0]
        server = self._director.clerk.getServers(id = setting.serverid )

        if not server:
            return link

        
        link = Link(label   = server.address,
                    Class   = "action-link",
                    tip     = "Show details of computational cluster",
                    onclick = select(id='').append(load(actor='server/load', routine='createDialog'))
                    )

        return link


if __name__ == "__main__":
    pass


__date__ = "$Nov 11, 2009 1:21:52 PM$"

