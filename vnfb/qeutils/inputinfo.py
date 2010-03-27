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

from vnfb.qeutils.qeconst import TYPE
from vnfb.qeutils.qeutils import latestInput

from luban.content import load
from luban.content.Link import Link

BASE        = "material_simulations/espresso-utils/"
DEFAULT_GEN = BASE + "generate-default" # Default generator actor

class InputInfo:
    """Displays input for simulation task"""

    def __init__(self, director, id, taskid, type):
        self._director  = director
        self._id        = id
        self._taskid    = taskid
        self._type      = type
        self._sim       = director.clerk.getQESimulations(id=id)


    def getLink(self):      # simulation
        inputs  = self._director.clerk.getQEConfigurations(where="taskid='%s'" % self._taskid )

        link    = self._linkAdd()
        if not inputs:      # No inputs created, return "Add" link
            return link

        input   = latestInput(inputs)
        if not input:       # No input, return "Add" link
            return link

        return Link(label   = input.filename,
                    onclick = load(actor      = "material_simulations/espresso/input-view",
                                 id         = self._id,
                                 taskid     = self._taskid,
                                 type       = self._type,
                                 configid   = input.id)   # Some more?
                    )


    # XXX: Make it more flexible
    def _linkAdd(self):
        "Returns link 'Add'"
        actor   = DEFAULT_GEN

        if self._type in TYPE:      # If task type is QE types
            actor   = getattr(self, "actor" + self._type)()  # Example: self._actorPW()

        link = Link(label="Add",
                    onclick=load(actor      = actor, 
                                 id         = self._id,
                                 taskid     = self._taskid,
                                 type       = self._type,
                                 simtype    = self._simType(),
                                 structureid    = self._structureId())
                    )
        return link


    def actorPW(self):
        return BASE + "generate-pw"

    def actorPH(self):
        return BASE + "generate-ph"

    def actorDOS(self):
        return BASE + "generate-dos"

    def actorQ2R(self):
        return BASE + "generate-q2r"

    def actorMATDYN(self):
        return BASE + "generate-matdyn"

    def actorDYNMAT(self):
        return BASE + "generate-dynmat"

    def actorBANDS(self):
        #return BASE + "generate-bands" # Not implemented
        return DEFAULT_GEN

    def actorPLOTBAND(self):
        #return BASE + "generate-plotbands"  # Not implemented
        return DEFAULT_GEN

    def actorPP(self):
        #return BASE + "generate-pp"    # Not implemented
        return DEFAULT_GEN

    def actorD3(self):
        #return BASE + "generate-d3" # Not implemented
        return DEFAULT_GEN


    def _simType(self):
        "Returns simulation type"
        if not self._sim:
            return ""

        return self._sim.type


    def _structureId(self):
        "Returns atomic structure id"
        if not self._sim:
            return ""

        return self._sim.structureid


if __name__ == "__main__":
    pass


__date__ = "$Dec 15, 2009 10:50:39 PM$"


