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

# Simple validator for PW input 
PWVALID    = {}
PWVALID["atomic_species"]   = 3     # Number of items in the line
PWVALID["atomic_positions"] = 4

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
    def atomicStructure(self):
        "Atom mass name: mass<number>, atom pseudo potential name: pseudo<number>"
        atoms       = QEGrid(lc.grid(Class="qe-table-atomic"))
        list        = self._atomsList()

        if not list:
            return "None"

        atoms.addRow(("#", "Atom", "Position (bohr)", "Mass (u)", "Pseudo-Potential"))

        for row in list:
            atoms.addRow((row[0], row[1], row[2], row[3], row[4]))

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

        if param is not None and param.isdigit() and int(param) in range(len(IBRAV)):
            return IBRAV[int(param)]

        return "None"   # default


    def energyCutoff(self):
        "system.ecutwfc"
        return self._energyParam("ecutwfc")


    def densityCutoff(self):
        "system.ecutrho"
        return self._energyParam("ecutrho")


    def smearingType(self):
        "smearing"
        return self._param("smearing")
    

    def smearingDegree(self):
        "degauss"
        return self._energyParam("degauss")


    # XXX: Not complete! There might be other forms of K points
    def kPoints(self):
        lines   = self._pwinput.card("k_points").lines()

        if len(lines) == 1:
            items   =  lines[0].split()
            if len(items) == 6:
                return "(%s, %s, %s)" % (items[0], items[1], items[2])
            
        return "None"


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


    def _energy(self, type):
        "Returns tuple (energy, unit) if energy is not None or None otherwise"
        if not self._pwtask:
            return None

        value   = self._pwoutput.property(type, withUnits=True)

        if value != (None, None):
            return (value[0][0], value[1])   # (energy, unit)

        return None


    # XXX: Combine with param?
    def _energyParam(self, type):
        param   = self._pwinput.namelist("system").param(type)
        return self._format((param, "Ry"))


    def _param(self, type, nl = "system"):
        param   = self._pwinput.namelist(nl).param(type)
        if param:
            return param

        return "None"


    def _format(self, energy):
        # Do energy formatting
        if energy and len(energy) == 2 and energy[0]:
            return  "%s %s" % (energy[0], energy[1])

        return "None"


    # XXX: Work on a better validation of code!
    def _atomsList(self):
        "Returns list of atoms with format:"
        # list.append(("1", "Fe", "(0.00, 0.00, 0.00)", "26.8", "Fe-blah-blah-blah-UPF"))
        positions   = self._atomicCard("atomic_positions", PWVALID)
        species     = self._atomicCard("atomic_species", PWVALID)

        if not positions or not species:    # Check if cards are in a proper form
            return None

        list        = []
        specDict    = self._speciesParams(species)

        for i in range(len(positions)):
            p       = positions[i]
            params  = specDict[p[0]]
            v   = ( str(i+1),
                    p[0],           # Example: "Al"
                    "(%.2f, %.2f, %.2f)" % (float(p[1]), float(p[2]), float(p[3])),
                    params[0],      # Example: "26.8"
                    params[1])      # Example: Al.blyp-n-van_ak.UPF
            list.append(v)

        return list


    # Move to card.py code?
    # XXX: Check if the validator has the name
    def _atomicCard(self, name, validator):
        items       = self._pwinput.card(name).lines()

        if not items:
            return None

        itemlist       = []
        for i in items:
            v       = i.split()
            if len(v) != validator[name]:     # Mulfunctioned input
                return None
            itemlist.append(v)

        return itemlist


    def _speciesParams(self, species):
        "Returns dicionary of species parameters"
        # Example: species = [("Al", "26.9815", "Al.blyp-n-van_ak.UPF"),]
        dict    = {}
        for s in species:
            key     = s[0]          # Example: "Al"
            if dict.has_key(key):   # Take only the first key
                continue

            dict[key]  = (s[1], s[2]) # Add key

        return dict


    # XXX: Refactor
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

