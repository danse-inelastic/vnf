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

class MATDYNGenerator(object):

    def __init__(self, director, inventory):
        self._inv       = inventory

        #self._simtype   = inventory.simtype     # Special case
        self._input     = input

    # XXX: nk points still should be present in the input file
    def _input(self, director):
        matdynInput = self._matdynInput(director)

        method      = self._subtype()
        if method == "dispersion":
            qpoints = self._qpoints(director, matdynInput)
            matdynInput.qpoints.set(qpoints)
            # Add nk points?
            nl  = matdynInput.namelists["input"]
            nl.add("nk1", self.nk1)
            nl.add("nk2", self.nk2)
            nl.add("nk3", self.nk3)

        return matdynInput.toString()


    def _subtype(self):
        "Returns subtype of simulation: 'dos' or 'dispersion'"
        methods     = MATDYN_METHOD.keys()
        option      = int(self.inventory.method)
        return methods[option]


    def _matdynInput(self, director):
        "Returns input object that can be later on used to add parameters"
        # E.g.: /home/dexity/espresso/qejobs/643E2QQI/ni.fc
        path    = remoteResultsPath(director, self.inventory.id, "Q2R")   #self._fcpath(director)
        path    = os.path.join(path, "%s.fc" % PREFIX)

        input   = MatdynInput()
        nl      = Namelist("input")
        nl.add("asr", self._asr(director))
        nl.add("flfrc", "'%s'" % path)
        nl.add("dos", ".true.")
        nl.add("nk1", self.nk1)
        nl.add("nk2", self.nk2)
        nl.add("nk3", self.nk3)

        # Add amasses
        list    = self._amasses(director)
        for m in list:
            nl.add(m[0], m[1])

        input.addNamelist(nl)
        return input


    # XXX: Take 'asr' parameter from Q2R instead of setting it manually
    def _asr(self, director):
        return "'crystal'"

    def _qpoints(self, director, mdinput):
        "Returns qpoints"
        pwdir       = self._pwpath(director)
        pwfile      = qeinput(director, self.id, "PW")
        pwpath      = packname(pwfile.id, "pw.in")
        pwpath      = os.path.join(pwdir, pwpath)
        pwInput     = PWInput(filename = pwpath)
        pwInput.parse()

        nl          = mdinput.namelist("input")
        # Populate grid
        nqGrid      = [int(nl.param("nk1")), int(nl.param("nk2")), int(nl.param("nk3"))]
        # XXX Handle case when parameters are not are not set
        qpoints     = kmesh.kMeshCart(nqGrid, pwInput.structure.lattice.reciprocalBase())

        return qpoints


    def _pwpath(self, director):
        # Example: pwdir   = "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTRqFuy/8CNH5MUJ"
        return resultsdir(director, self.id, "PW")    # tmp results directory


    # Copied from generate-phr.py
    def _amasses(self, director):
        """Returns list of tuples with amass label and mass value from PW input configuration
        Example: [("amass(1)", "35.5"), ("amass(2)", "54.3")]
        """
        list    = []    # amass list
        masses  = self._masses(director)
        for l in range(len(masses)):
            list.append(("amass(%s)" % str(l+1), masses[l][1]))

        return list

    # Copied from generate-q2r.py
    def _masses(self, director):
        # PW configuration input
        pwinput     = inputRecord(director, self.inventory.id, "PW")
        fname       = defaultInputName(pwinput.type)
        text        = readRecordFile(director.dds, pwinput, fname)
        pw          = QEInput(config = text)
        pw.parse()

        list        = []
        # List of atom of format: [('Ni', '52.98', 'Ni.pbe-nd-rrkjus.UPF'), (...)]
        atoms       = pw.structure()
        for a in atoms:
            list.append((a[0], a[1]))

        return list

    

__date__ = "$Mar 24, 2010 9:59:39 AM$"


