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

from vnfb.qeutils.results.qeresult import QEResult
from vnfb.qeutils.qeconst import SMEARING, IBRAV
from vnfb.qeutils.qegrid import QEGrid

from qecalc.qetask.pwtask import PWTask
import luban.content as lc

# Simple validator for PW input 
PWVALID     = {}
PWVALID["atomic_species"]   = 3     # Number of items in the line
PWVALID["atomic_positions"] = 4
NONE        = "None"

class PWResult(QEResult):

    def __init__(self, director, simid):     # simulation id
        self._type  = "PW"  # Important attribute
        super(PWResult, self).__init__(director, simid, self._type)


    def _taskFactory(self, input, output):
        config  = "[pw.x]\npwInput: %s\npwOutput: %s" % (input, output)
        return PWTask(configString=config)


    # Input methods
    def atomicStructure(self):
        "Atom mass name: mass<number>, atom pseudo potential name: pseudo<number>"
        atoms       = QEGrid(lc.grid(Class="qe-table-atomic"))
        list        = self._atomsList()

        if not list:
            return "None"

        atoms.addRow((" ", "Atom", "Position (bohr)", "Mass (u)", "Pseudo-Potential"))

        for row in list:
            atoms.addRow((row[0], row[1], row[2], row[3], row[4]))

        atoms.setRowStyle(0, "qe-table-header") 
        return atoms.grid()


    # XXX: Fix issue with aliaces
    def materialType(self):
        "Material type"
        param   = self._nlparam("system", "occupations") 

        if param == "'fixed'":
            return "Isolator"

        # Check deeper for smearing
        smparam = self._nlparam("system", "smearing")
        if smparam in SMEARING.values():
            return "Metal"  

        return "None"   # default


    def latticeType(self):
        param   = self._nlparam("system", "ibrav")

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
        return self._nlparam("system", "smearing")
    

    def smearingDegree(self):
        "degauss"
        return self._energyParam("degauss")


    # XXX: Not complete! There might be other forms of K points
    def kPoints(self):
        lines   = self._cardlines("k_points")

        if lines and len(lines) == 1:
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
        "Returns formatted force vector for each atom"
        if not self._output:    # No output
            return NONE

        forces  = self._outputForces()
        if not forces:          # No forces in the output
            return NONE
        
        table    = QEGrid(lc.grid(Class="qe-table-forces"))
        table.addRow((" ", "Atom", "Force (Ry/bohr)"))
        
        for f in forces:
            table.addRow((f[0], f[1], "(%.2f, %.2f, %.2f)" % (f[2], f[3], f[4]) ))

        table.setRowStyle(0, "qe-table-header")
        return table.grid()


    def stress(self):
        "Returns formatted stress"
        if not self._output:    # No output
            return NONE

        stress  = self._outputStress()
        if not stress:          # No stress in the output
            return NONE

        table    = QEGrid(lc.grid(Class="qe-table-stress"))
        for s in stress:
            table.addRow(("%.2f %.2f %.2f" % (s[0], s[1], s[2]) ))

        return table.grid()


    # Specific for geometry optimization
    def latticeInput(self):
        "Lattice structure"
        if not self._output:    # No output
            return NONE

        table    = QEGrid(lc.grid(Class="qe-table-forces"))
        table.addRow(("A", "B", "C", "cosAB", "cosBC"))
        table.addRow(("6.56", "6.56", "6.56", "0.67", "0.78"))
        table.setRowStyle(0, "qe-table-header")

        return table.grid()


    # Auxiliary methods
    def _energy(self, type):
        "Returns tuple (energy, unit) if energy is not None or None otherwise"
        if not self._task:
            return None

        value   = self._output.property(type, withUnits=True)

        if value != (None, None):
            return (value[0][0], value[1])   # (energy, unit)

        return None


    def _energyParam(self, type):
        param   = self._nlparam("system", type)
        return self._format((param, "Ry"))


    def _outputForces(self):
        "Returns output forces"
        forces  = []
        atoms   = self._atomLabels()
        foutput = self._output.property("forces", withUnits=True)
        fvector = foutput[0]    # Force vector. Example: ((0.0, 0.0, 0.0), (0.5, 0.5, 0.5))
        assert len(atoms) == len(fvector)   # validate?
        for i in range(len(fvector)):
            f   = fvector[i]
            forces.append((str(i+1), atoms[i], f[0], f[1], f[2]))

        if len(forces) == 0:
            return None     # Keep interface similar to stress
        
        return forces       # Example: [("1", "Al", 0.00, 0.00, 0.00), [...]]


    def _outputStress(self):
        "Returns output stress in format 3x3: ([0.00, 0.00, 0.00], [...])"
        soutput = self._output.property("stress", withUnits=True)
        return soutput[0]   # ([0.0, 0.0, 0.0], [...], [...])


    def _nlparam(self, nl, param, formatted=False):
        "Returns parameter of the namelist nl"
        if self._input:
            p   = self._input.namelist(nl).param(param)
            if p:
                return p

        if formatted:
            return "None"

        return None


    def _cardlines(self, name):
        "Return list of card lines"
        if self._input:
            return self._input.card(name).lines()

        return None # No formatting


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


    def _atomLabels(self):
        atoms       = []
        atomlist    = self._atomsList()
        for a in atomlist:
            atoms.append(a[1])

        return atoms


    # Move to card.py code?
    # XXX: Check if the validator has the name
    def _atomicCard(self, name, validator):
        items       = self._cardlines(name) #self._input.card(name).lines()

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


__date__ = "$Mar 15, 2010 2:45:52 PM$"

