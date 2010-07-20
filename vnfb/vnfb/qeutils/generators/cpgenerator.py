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

from vnfb.qeutils.results.cpresult import CPResult
from vnfb.qeutils.qeparser.qeinput import QEInput
from vnfb.qeutils.qeutils import defaultInputName, readRecordFile


EM_LINKORDER    = 0 # Electron minimization should exist!

class CPGenerator(object):
    "Generator for CP molecular dynamics tasks"

    def __init__(self, director, inventory, input = None):
        self._director  = director
        self._inv       = inventory
        self._input     = input
        self._init()


    def setInput(self):
        "Update input"
        self.setControl()
        self.setSystem()
        self.setElectrons()
        self.setIons()
        self.setCell()
        self.setExtra()


    # Methods which should be overwritten in subclasses!
    def setControl(self):
        "CONTROL namelist"
        pass


    def setSystem(self):
        "SYSTEM namelist"
        pass


    def setElectrons(self):
        "ELECTRONS namelist"
        pass


    def setIons(self):
        "IONS namelist"
        pass


    def setCell(self):
        "CELL namelist"
        pass


    def setExtra(self):
        "Extra parameters not specified by other namelists or cards"
        pass

    def _init(self):
        self._inputFromRecord()
        # Note:
        #   - Change to _inputFromResult() if you want to get input from result!


    def _inputFromRecord(self):
        "Set input object from input configuration"
        inputs  = self._director.clerk.getQEConfigurations(where="taskid='%s'" % self._emTaskId())
        if len(inputs) == 0:    # No input created
            return

        input       = inputs[0]
        fname       = defaultInputName(input.type)
        inputStr    = readRecordFile(self._director.dds, input, fname)
        self._input = QEInput(config = inputStr, type = "cp")
        self._input.parse()


    def _inputFromResult(self):
        "Set input object from electron-min result"
        if not self._input:
            self._input = self._cpInput()


    def _cpInput(self):
        "Take input file from results and create QEInput object"
        result      = CPResult(self._director, self._inv.id, linkorder = EM_LINKORDER)
        return result.input()


    def _emTaskId(self):
        "Returns electron-min task id"
        simtasks    = self._director.clerk.getQESimulationTasks(where="simulationid='%s'" % self._inv.id)
        for st in simtasks:
            if st:
                task    = self._director.clerk.getQETasks(id=st.taskid)
                if task.linkorder == 0:
                    return task.id

        return None


    def toString(self):
        if not self._input:
            return "CP Generator: Electronic Minimization input is not created!"

        return self._input.toString()


# Keep the code, in case if CPTask works incorrectly
#        inputFile   = result.inputFile()
#        input = QEInput(filename = inputFile, type = "cp")
#        input.parse()
#        return input


__date__ = "$May 18, 2010 1:24:49 AM$"


