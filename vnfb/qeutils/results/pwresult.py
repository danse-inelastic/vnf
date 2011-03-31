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

from vnf.qeutils.results.qeresult import QEResult
from vnf.qeutils.qeconst import SMEARING, IBRAV
from vnf.qeutils.qegrid import QEGrid
from vnf.qeutils.qeutils import fstr

from qecalc.qetask.pwtask import PWTask
import luban.content as lc

# Constants
A2B             = 1.889725989   # Angstroms to bohrs
PI              = 3.14159265

# Simple validator for PW input 
PWVALID     = {}
PWVALID["atomic_species"]   = 3     # Number of items in the line
PWVALID["atomic_positions"] = 4
NONE        = "None"

class PWResult(QEResult):

    def __init__(self, director, simid, linkorder = 0, job = None):
        super(PWResult, self).__init__(director, simid, linkorder, job=job)


    def _taskFactory(self):
        config  = "[pw.x]\npwInput: %s\npwOutput: %s" % (self._inputFile, self._outputFile)
        return PWTask(configString=config)


    # Input methods
    def atomicStructure(self):
        "Atom mass name: mass<number>, atom pseudo potential name: pseudo<number>"
        atoms       = QEGrid(lc.grid(Class="qe-table-atomic"))
        list        = self._atomsList()

        if not list:
            return NONE

        atoms.addRow(("Atom", "Position (bohr)", "Mass (u)", "Pseudo-Potential"))

        for row in list:
            atoms.addRow((row[1], row[2], row[3], row[4]))

        atoms.setRowStyle(0, "qe-table-header-left")
        return atoms.grid()


    # XXX: Fix issue with aliaces
    def materialType(self):
        "Material type"
        if self.isIsolator():
            return "Isolator"

        # Check deeper for smearing
        smparam = self._nlparam("system", "smearing")
        if smparam in SMEARING.values():
            return "Metal"  

        return NONE   # default


    def latticeType(self):
        param   = str(self._nlparam("system", "ibrav"))

        if param is not None and param.isdigit() and int(param) in range(len(IBRAV)):
            return IBRAV[int(param)]

        return NONE   # default


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
    def kPoints(self, formatted=True):
        "Returns list of k-points if formatted == True, string - otherwise"
        lines   = self._cardlines("k_points")
        kp      = None    # k-points

        if lines and len(lines) == 1:
            items   =  lines[0].split()
            assert len(items) == 6  # Example: item = ["4", "4", "4", "0", "0", "0"]
            kp  = (int(items[0]), int(items[1]), int(items[2]))

        if not formatted:   # no formatting, return just list of k-points
            return kp

        # Formatting
        if not kp:
            return NONE

        return "(%s, %s, %s)" % (kp[0], kp[1], kp[2])


    # Output methods
    def totalEnergy(self, formatted=False):
        "Return total energy"
        energy  = self._energy('total energy')

        if not formatted:    # No formatting
            return energy

        return self._format(energy)


    def fermiEnergy(self, formatted=False):
        "Return fermi energy"
        energy  = self._energy('fermi energy')

        if not formatted:    # No formatting
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
        table.addRow(("Atom", "Force (Ry/bohr)"))
        
        for f in forces:
            table.addRow((f[1], "%.2f, %.2f, %.2f" % (f[2], f[3], f[4]) ))

        table.setRowStyle(0, "qe-table-header-left")
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
        "Lattice output structure"
        lp   = self._inputLatticeParams()
        return self._latticeTable(lp)


    # Specific for geometry optimization
    def latticeOutput(self):
        "Lattice output structure"
        lp   = self._outputLatticeParams()
        return self._latticeTable(lp)


    def positionInput(self):
        "Returns input positions"
         # From ATOMIC_POSITIONS card of input file
        poslist     = []
        positions   = self._atomicCard("atomic_positions", PWVALID)
        for p in positions:
            poslist.append((p[0], [float(p[1]), float(p[2]), float(p[3])]))

        # XXX: Not sure if the code is correct
        #self._input.structure.parseInput()
        #struct  = self._input.structure.structure
        #poslist = zip(struct.symbols, struct.xyz)
        return self._position(poslist)


    def positionOutput(self):
        #poslist = [("Fe", [0, 0, 0]), ("Fe", [0, 0.5, 0])]
        self._input.structure.parseOutput(self._outputFile)
        struct  = self._input.structure.structure
        poslist = zip(struct.symbols, struct.xyz)
        return self._position(poslist)

#   Cartesian axes
#
#     site n.     atom                  positions (a_0 units)
#         1           Al  tau(  1) = (   0.0000000   0.0000000   0.0000000  )
#         2           Al  tau(  2) = (   2.0200000   3.2320000   0.0000000  )
#         3           Al  tau(  3) = (   2.0200000   0.0000000   2.0200000  )
#         4           Al  tau(  4) = (   0.0000000   2.0200000   2.0200000  )


    def species(self):
        "Returns list of species in format: [('Al', '26.9815', 'Al.blyp-n-van_ak.UPF'),]"
        return self._atomicCard("atomic_species", PWVALID)


    def isIsolator(self):
        "Checks if material is isolator looking into the 'occupations' parameter"
        try:
            # If no parameters found, it raises exception. Fix Namelist class
            occupations   = self._input.namelist("system").param("occupations", quotes=False)
        except:
            return False

        if occupations == "fixed":  # "fixed" value is used for isolators only!
            return True
        
        return False


    def recipLattice(self):
        "Returns reciprocal lattice"
        if not self._input:
            return None     # No PW input, not reciprocal lattice

        return self._input.structure.lattice.diffpy().reciprocal().base*2.0*PI*A2B


    # Specific for geometry optimization
    def _latticeTable(self, lp):
        "Takes lattice parameters and returns formatted table of lattice structure"
        if not self._output:    # No output
            return NONE

        table    = QEGrid(lc.grid(Class="qe-table-forces"))
        table.addRow(("A", "B", "C", "cosAB", "cosAC", "cosBC"))
        table.addRow(self._fstr(lp))
        table.setRowStyle(0, "qe-table-header-left")
        return table.grid()


    def _position(self, poslist):
        "Returns formatted structure of atomic positions"
        # Example: poslist = [('a', [0, 0, 0]), ('b', [1, 1, 1])]
        if not self._output:    # No output
            return NONE

        table    = QEGrid(lc.grid(Class="qe-table-forces"))
        table.addRow(("Atom", "Coordinates"))
        for pl in poslist:
            table.addRow((pl[0], "%.2f, %.2f, %.2f" % (pl[1][0], pl[1][1], pl[1][2])))
        
        table.setRowStyle(0, "qe-table-header-left")
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

        if not fvector: # No force vector, no output forces!
            return None
        
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
            p   = self._input.namelist(nl).get(param)
            if p:
                return p

        if formatted:
            return NONE

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

        return NONE


    # XXX: Work on a better validation of code!
    def _atomsList(self):
        "Returns list of atoms with format:"
        # list.append(("1", "Fe", "0.00, 0.00, 0.00", "26.8", "Fe-blah-blah-blah-UPF"))
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
                    "%.2f, %.2f, %.2f" % (float(p[1]), float(p[2]), float(p[3])),
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
        items       = self._cardlines(name)

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


    def _inputLatticeParams(self):
        "Return input lattice parameters"
        self._input.parse() # Populate lattice from input config file
        return self._latticeParams()


    def _outputLatticeParams(self):
        "Return output lattice parameters"
        # Weird interface
        self._input.structure.parseOutput(self._outputFile) # Populate lattice from output config file
        return self._latticeParams()

        
    def _latticeParams(self):
        "Returns tuple of float lattice parameters for input and output config files"
        l   = self._lattice()
        if not l:
            return None

        return (l.a, l.b, l.c, l.cAB, l.cAC, l.cBC)


    def _lattice(self):
        "Returns QELattice object composed of diffpyStructure/matter lattice"
        # See qecalc.qetask.qeparser.qelattice.py
        try:
            lattice = self._input.structure.lattice
        except AttributeError:
            lattice = None

        return lattice


    def _fstr(self, flist):
        "Takes list of float numbers and converts them to formatted string"
        lp  = []
        for l in flist:
            lp.append(fstr(l))

        return lp



__date__ = "$Mar 15, 2010 2:45:52 PM$"

