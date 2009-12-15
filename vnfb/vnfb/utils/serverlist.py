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
        self._setServers(director)


    def _setServers(self, director):
        "Set servers dictionary {id: short_description} from the database"
        servers     = director.clerk.getServers()
        self._servers = OrderedDict()
        for s in servers:
            self._servers[s.id]    = s.address

        return self._servers


    def list(self):
        "Returns list of server names"
        return self._servers.values()


    def id(self, i):
        "Return server's id"
        keys    = self._servers.keys()
        return keys[int(i)]


__date__ = "$Dec 14, 2009 5:32:06 PM$"


# *********** DEAD CODE ******************

#        #if len(keys) < i + 1 and i >= 0:
#        #    return None
#        # Check if i-th element is present

