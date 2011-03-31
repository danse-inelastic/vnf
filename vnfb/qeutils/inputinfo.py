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

from vnf.qeutils.qeconst import QETYPES, SIMCHAINS
from vnf.qeutils.qeutils import latestInput, noHyphen, getResult
from vnf.qeutils.results.phresult import PHResult

from luban.content import load, alert
from luban.content.Link import Link

BASE        = "material_simulations/espresso-utils/"
GENERATOR   = BASE + "generate-default"     # Default generator actor
ROUTINE     = "default"                     # Default routine

class InputInfo:
    """Displays input for simulation task"""

    def __init__(self, director, id, taskid, type, linkorder):
        self._director  = director
        self._id        = id            # simulation id
        self._taskid    = taskid
        self._type      = type
        self._linkorder = linkorder
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


    def _linkAdd(self):
        "Returns link 'Add'"
        (actor, routine)   = (GENERATOR, ROUTINE)

        if self._type in QETYPES:      # If task type is QE types
            (actor, routine)   = getattr(self, "locator" + self._routineExt())()  # Example: self.locatorPW()

        try:
            linkorder   = int(self._linkorder)  # should be int, but just in case
        except:
            linkorder   = -1

        # NEEDS TESTING!!!
        # There might be a problem that result.outputFile() is empty although
        # the results are retrieved. This happened (for some reason).
        # If it continues to fail fix outputFile() or try to use JobStatus instead
        result  = getResult(self._director, self._id, self._sim, linkorder-1)  # Previous result

        if linkorder == 0 or (result != None and result.outputFile()):  # First task or results are retrieved!
            link = Link(label="Add",
                        onclick=load(actor      = actor,
                                     routine    = routine,
                                     id         = self._id,
                                     taskid     = self._taskid,
                                     type       = self._type,
                                     simtype    = self._simType(),
                                     linkorder  = self._linkorder,
                                     structureid    = self._structureId())
                        )
        else:
            prevtask    = ""
            if self._sim and self._sim.type in SIMCHAINS.keys() and linkorder >= 1:
                prevtask    = SIMCHAINS[self._sim.type][linkorder-1]  # Find type of previous task

            link  = Link(label="Add",
                         onclick=alert('Please run simulation or retrieve (check) result for previous %s task. When result is retrieved, make sure to click on "Refresh Status"' % prevtask))


        return link


    def _routineExt(self):
        return noHyphen(self._type)


    def locatorPW(self):
        routine = ROUTINE
        if self._linkorder == 1:        # For the second PW go directly to input creation form
            routine = "generateNscfInput"

        return (BASE + "generate-pw", routine)


    def locatorPH(self):
        return (BASE + "generate-ph", ROUTINE)


    def locatorDOS(self):
        return (BASE + "generate-dos", ROUTINE)


    def locatorQ2R(self):
        return (BASE + "generate-q2r", ROUTINE)


    def locatorMATDYN(self):
        return (BASE + "generate-matdyn", ROUTINE)


    def locatorDYNMAT(self):
        routine     = ROUTINE
        phresult    = PHResult(self._director, self._id)

        if not phresult.isGammaPoint():     # For not gamma point go directly to input creation form
            routine = "generateInput"

        return (BASE + "generate-dynmat", routine)


    def locatorBANDS(self):
        return (BASE + "generate-bands",  "generateInput")


    def locatorPLOTBAND(self):
        return (BASE + "generate-plotband", ROUTINE)


    def locatorPP(self):
        #return BASE + "generate-pp"    # Not implemented
        return self._locatorDefault()


    def locatorD3(self):
        #return BASE + "generate-d3" # Not implemented
        return self._locatorDefault()


    # Molecular dynamics specific locators
    def locatorelectronmin(self):
        return (BASE + "generate-electron-min", ROUTINE)


    def locatorionmin(self):
        return (BASE + "generate-ion-min", ROUTINE)


    def locatorionrandom(self):
        return (BASE + "generate-ion-random", ROUTINE)


    def locatorquenching(self):
        return (BASE + "generate-quenching", ROUTINE)


    def locatordynamics(self):
        return (BASE + "generate-dynamics", ROUTINE)


    def locatorthermostat(self):
        return (BASE + "generate-thermostat", ROUTINE)


    def locatortrajectory(self):
        return (BASE + "generate-trajectory", ROUTINE)


    def _locatorDefault(self):
        "Default locator"
        return (GENERATOR, "generateInput")


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


