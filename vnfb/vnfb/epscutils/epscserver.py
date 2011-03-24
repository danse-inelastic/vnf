# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                               Alex Dementsov
#                      California Institute of Technology
#                        (C) 2011  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from luban.content import load, select
from luban.content.Link import Link

class EPSCServer:

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

__date__ = "$Mar 23, 2011 4:58:57 PM$"


