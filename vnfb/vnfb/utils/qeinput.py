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

from luban.content import load
from luban.content.Link import Link


class QEInput:
    """Displays input for simulation task"""

    def __init__(self, director, taskid, type):
        self._director  = director
        self._taskid    = taskid
        self._type      = type

    def getLink(self):      # simulation
        inputs  = self._director.clerk.getQEConfigurations(where="taskid='%s'" % self._taskid )

        link = Link(label="Add", 
                    onclick=load(actor      = "material_simulations/espresso/input-add",
                                 taskid     = self._taskid,
                                 type       = self._type)   # Some more?
                    )

        if inputs:
            s = inputs[0]
            if s:
                link = Link(label=s.filename,
                            onclick=load(actor      = "material_simulations/espresso/input-view",
                                         id         = self._taskid,
                                         configid   = s.id)   # Some more?
                            )

        return link


if __name__ == "__main__":
    pass


__date__ = "$Dec 15, 2009 10:50:39 PM$"


