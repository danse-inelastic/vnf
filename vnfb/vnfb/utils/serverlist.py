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

from vnfb.utils.orderedDict import OrderedDict

class ServerList:
    """
    ServerList - is a simple utility that helps to display servers list in the form
    """
    def __init__(self, director):
        #self._setServers(director)
        self._setFixedServers(director)

    def list(self):
        "Returns list of server names"
        return self._servers.values()


    def id(self, selected):
        "Returns server's id from the number of selected option"
        keys    = self._servers.keys()
        return keys[int(selected)]  # What if selected is out of range?


    def selected(self, id):
        "Returns number of selected option from id. Opposite to self.id()"
        keys    = self._servers.keys()
        for k in range(len(keys)):
            if keys[k] == id:
                return k

        return 0


    def _setServers(self, director):
        "Set servers dictionary {id: short_description} from the database"
        servers     = director.clerk.getServers()
        self._servers = OrderedDict()
        for s in servers:
            self._servers[s.id]    = s.address

        return self._servers

    def _setFixedServers(self, director):
        "Uses fixed server (in case if you don't need other servers)"
        server     = director.clerk.getServers(id="server001")
        self._servers = OrderedDict()
        self._servers[server.id]    = server.address
        return self._servers


__date__ = "$Dec 14, 2009 5:32:06 PM$"


