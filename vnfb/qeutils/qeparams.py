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


class QEParams:
    """Displays parameters of the simulation"""

    def __init__(self, sim, director):
        self._sim     = sim
        self._director  = director


    def getLink(self, id):      # simulation
        settings  = self._director.clerk.getQESettings(where="simulationid='%s'" % id )

        link = Link(label="Add", Class="action-link",
                    tip     = "Set simulation environment",
                    onclick=load(actor      = "material_simulations/espresso/settings-add",
                                 type       = self._sim.type,
                                 id         = id,
                                 )
                    )

        if settings:
            s = settings[0]
            if s:
                link = Link(label   = s.sname, Class="action-link",
                            onclick = load(actor    = "material_simulations/espresso/settings-view",
                                         id         = id,
                                         configid   = s.id)
                            )

        return link


if __name__ == "__main__":
    chain   = QEParams(None)



__date__ = "$Nov 10, 2009 5:52:02 PM$"



