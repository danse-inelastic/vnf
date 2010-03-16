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

import os
from vnfb.qeutils.qeutils import dataroot, defaultInputName
from vnfb.qeutils.qeconst import OUTPUT_EXT, SMEARING, IBRAV
from vnfb.qeutils.qeresults import QEResults
from vnfb.qeutils.qetaskinfo import TaskInfo
from vnfb.qeutils.qegrid import QEGrid
from vnfb.qeutils.qerecords import SimulationRecord

from qecalc.qetask.pwtask import PWTask

import luban.content as lc

class PWResult(object):

    def __init__(self, director, simid):     # simulation id
        self._director      = director
        self._simid         = simid

        # Attributes
        self._pwtask         = None     # Will remain None if output file is not available
        self._init()


    def _init(self):
        "Retrieve output file and parse it"
        input       = self._resultFile("input")    # Input file
        output      = self._resultFile("output")   # Output file

        # Important line! No output file, no results!
        if not output: 
            return

        config          = "[pw.x]\npwInput: %s\npwOutput: %s" % (input, output)
        self._pwtask    = PWTask(configString=config)  # Need pwtask?
        self._pwinput   = self._pwtask.input
        self._pwoutput  = self._pwtask.output
        
        self._pwinput.parse()
        self._pwoutput.parse()
        

    # Input methods
    # STUB
    def atomicStructure(self):
        "Atom mass name: mass<number>, atom pseudo potential name: pseudo<number>"
        atoms    = QEGrid(lc.grid(Class="qe-table-atomic"))
        atoms.addRow(("#", "Atom", "Position (bohr)", "Mass (u)", "Pseudo-Potential"))
        atoms.addRow(("1", "Fe", "(0, 0, 0)", "26.8", "Fe-blah-blah-blah-UPF"))
        atoms.addRow(("2", "V", "(0.5, 0.5, 0.5)", "26.8", "V-blah-UPF"))
        atoms.addRow(("3", "V", "(0.75, 0.25, 0.35)", "26.8", "V-blah-UPF"))

#        for l in range(len(self._labels)):
#            label       = self._labels[l]
#            atom        = Atom(label)
#            mass        = FormTextField(name = "mass%s" % l, value = atom.mass, Class="mass-textfield")
#            pseudo      = FormSelectorField(name    = "pseudo%s" % l,
#                                            Class   = "qe-selector-pseudo",
#                                            entries = enumerate(PSEUDO[label]))
#            atoms.addRow((label, mass, pseudo))

        atoms.setRowStyle(0, "qe-table-header") 
        return atoms.grid()


    def materialType(self):
        param   = self._pwinput.namelist("system").param("occupations", quotes = False)
        if param == "fixed":
            return "Isolator"

        if param in SMEARING.keys():
            return "Metal"  

        return "None"   # default


    def latticeType(self):
        param   = self._pwinput.namelist("system").param("ibrav")
        #param   = int(param)
        if param is not None and param.isdigit() and int(param) in range(len(IBRAV)):
            return IBRAV[int(param)]

        return "None"   # default


    def energyCutoff(self):
        return "27.0 Ry"


    def densityCutoff(self):
        return "300 Ry"


    def smearingType(self):
        "smearing"
        return "gaussian"


    def smearingDegree(self):
        return "0.02 Ry"

    def kPoints(self):
        return "(8, 8, 8)"


    # Output methods
    def totalEnergy(self, formated=False):
        "Return total energy"
        energy  = self._energy('total energy')

        if not formated:    # No formatting
            return energy

        return self._format(energy)


    def fermiEnergy(self, formated=False):
        "Return fermi energy"
        energy  = self._energy('fermi energy')

        if not formated:    # No formatting
            return energy

        return self._format(energy)


    def forces(self):
        table    = QEGrid(lc.grid(Class="qe-table-forces"))
        table.addRow(("#", "Atom", "Force (Ry/bohr)"))
        table.addRow(("1", "Fe", "(0, 0, 0)"))
        table.addRow(("2", "V", "(0.5, 0.5, 0.5)"))
        table.addRow(("3", "V", "(0.75, 0.25, 0.35)"))

        table.setRowStyle(0, "qe-table-header")
        return table.grid()


    def stress(self):
        table    = QEGrid(lc.grid(Class="qe-table-stress"))
        table.addRow(("0.50000000", "0.50000000", "0.50000000"))
        table.addRow(("0.50000000", "0.50000000", "0.50000000"))
        table.addRow(("0.50000000", "0.50000000", "0.50000000"))

        return table.grid()

        #return "0.0 0.0 0.0"

    def _energy(self, type):
        "Returns tuple (energy, unit) if energy is not None or None otherwise"
        if not self._pwtask:
            return None

        value   = self._pwoutput.property(type, withUnits=True)

        if value != (None, None):
            return (value[0][0], value[1])   # (energy, unit)

        return None


    def _format(self, energy):
        # Do energy formatting
        if energy:
            return  "%s %s" % (energy[0], energy[1])

        return "None"


    def _resultFile(self, type="input"):
        "Retruns absolute path of the PW result file, e.g. output or input config files"
        # Example: "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTsdw21/4ICDAVNK/4I2NPMY4pw.in.out"
        
        simrecord   = SimulationRecord(self._director, self._simid)
        jitlist     = simrecord.jobInputTaskList()

        for jit in jitlist:
            # jit   = (job, input, task) = (jit[0], jit[1], jit[2])
            _job     = jit[0]
            _input   = jit[1]
            _task    = jit[2]
            if _job is None:   # If job is None
                continue

            if _input and _task.type == "PW":   # PW type
                datadir     = dataroot(self._director)
                taskinfo    = TaskInfo(simid = self._simid, type = "PW")
                results     = QEResults(self._director, _job, taskinfo)
                if results.ready():
                    file        = "%s%s" % (_input.id, defaultInputName(_task.type))
                    if type == "output":
                        file    += OUTPUT_EXT   # .out
                    path        = os.path.join(results.tardir(), file)
                    return os.path.join(datadir, path)

        return None


__date__ = "$Mar 15, 2010 2:45:52 PM$"

