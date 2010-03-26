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
GEN_DEFAULT = BASE + "generate-default" # Default generator actor

class InputInfo:
    """Displays input for simulation task"""

    def __init__(self, director, id, taskid, type):
        self._director  = director
        self._id        = id
        self._taskid    = taskid
        self._type      = type


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
        sim     = self._director.clerk.getQESimulations(id = self._id)
        actor   = GEN_DEFAULT

        if self._type in TYPE:      # If task type is QE types
            actor   = getattr(self, "actor" + self._type)()  # Example: self._actorPW()

        link = Link(label="Add",
                    onclick=load(actor      = actor, #"material_simulations/espresso/input-generate",
                                 id         = self._id,
                                 taskid     = self._taskid,
                                 type       = self._type,
                                 structureid    = sim.structureid)
                    )
        return link


    def actorPW(self):
        return BASE + "generate-pw"

    def actorPH(self):
        pass

    def actorBANDS(self):
        pass

    def actorPLOTBAND(self):
        pass

    def actorPP(self):
        pass

    def actorDOS(self):
        pass

    def actorQ2R(self):
        pass

    def actorMATDYN(self):
        pass

    def actorDYNMAT(self):
        pass

    def actorD3(self):
        pass



#TYPE        = {"PW":        "pw.x",
#               "PH":        "ph.x",
#               "BANDS":     "bands.x",
#               "PLOTBAND":  "plotband.x",
#               "PP":        "pp.x",
#               "DOS":       "dos.x",
#               "Q2R":       "q2r.x",
#               "MATDYN":    "matdyn.x",
#               "DYNMAT":    "dynmat.x",
#               "D3":        "d3.x"

#    def _simType(self, director):
#        "Returns simulation type"
#        sim     = director.clerk.getQESimulations(id=self.id)
#        if not sim:
#            return ""
#
#        return sim.type


if __name__ == "__main__":
    pass


__date__ = "$Dec 15, 2009 10:50:39 PM$"


