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

from luban.content import load
from luban.content.Link import Link


class EPSCSettings:
    """Displays settings of the simulation"""

    def __init__(self, sim, director):
        self._sim     = sim
        self._director  = director


    def getLink(self, id):      # simulation
        settings  = self._director.clerk.getQESettings(where="simulationid='%s'" % id )

        # Default link
        link = Link(label="Add", Class="action-link",
                    tip     = "Set simulation environment",
                    onclick=load(actor      = "material_simulations/epsc/settings-add",
                                 id         = id)
                    )

        if settings:
            s = settings[0]
            if s:
                link = Link(label   = s.sname, Class="action-link",
                            onclick = load(actor    = "material_simulations/epsc/settings-view",
                                         id         = id,
                                         configid   = s.id)
                            )

        return link

__date__ = "$Mar 23, 2011 4:46:26 PM$"


