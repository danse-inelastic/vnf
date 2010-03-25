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
from vnfb.qeutils.results.q2rresult import Q2RResult
from vnfb.qeutils.qeconst import MATDYN_METHOD_LIST
from vnfb.qeutils.qeutils import qeinput, packname, resultsdir

from qecalc.qetask.qeparser.pwinput import PWInput
from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.results.pwresult import PWResult
from vnfb.qeutils.generators.phgenerator import PHGenerator

from qecalc.qetask.qeparser.matdyninput import MatdynInput
from vnfb.qeutils.qecalcutils import kmesh

#from vnfb.qeutils.qeparser.qeinput import QEInput
#from vnfb.qeutils.qeutils import remoteResultsPath
#from vnfb.qeutils.qeutils import inputRecord, readRecordFile, defaultInputName

DOS     = ".true."

class MATDYNGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._subtype   = None      # 'dos' or 'dispersion'
        self._input     = None

        self._init()


    def _init(self):
        "Additional init"
        method  = int(self._inv.method) # 0, 1
        if not method in range(len(MATDYN_METHOD_LIST)):  # if out of range
            return

        self._subtype   = MATDYN_METHOD_LIST[method]


    # XXX: nk points still should be present in the input file
    def setInput(self):
        "Populate 'input' namelist"
        q2rresult       = Q2RResult(self._director, self._inv.id)
        phgen           = PHGenerator(self._director, self._inv)
        self._input     = MatdynInput()
        nl              = Namelist("input") # Create namelist
        self._input.addNamelist(nl)

        nl.add("asr",   q2rresult.zasr())   # from Q2R result
        nl.add("flfrc", q2rresult.flfrc())  # from Q2R result
        nl.add("dos",   DOS)
        nl.add("nk1",   self._inv.nk1)
        nl.add("nk2",   self._inv.nk2)
        nl.add("nk3",   self._inv.nk3)

        # Add amasses
        masses    = phgen.amasses() # from PH generator

        if not masses:  # In case if not masses are found in PW input
            nl.add("amass", "ERROR: masses not defined in PW input file!")
            return

        for m in masses:
            nl.add(m[0], m[1])

        if not self._subtype:   # No subtype, no additional parameters
            return  

        # Generate k-points
        if self._subtype == "dispersion":
            self._input.qpoints.set(self._qpoints())
            # Force adding nk1, nk2, nk3 to input
            # This will later be used for exporting dispersion to atomic structure
            nl  = self._input.namelist("input")
            nl.add("nk1",   self._inv.nk1)
            nl.add("nk2",   self._inv.nk2)
            nl.add("nk3",   self._inv.nk3)


    def toString(self):
        return self._input.toString()


    def _qpoints(self):
        "Returns qpoints"
        pwresult    = PWResult(self._director, self._inv.id)
        kp          = pwresult.kPoints(formatted=False)
        if not kp:      # No k-points, no q-points
            return

        nqGrid      = [kp[0], kp[1], kp[2]]
        pwinput     = pwresult.input()
        return kmesh.kMeshCart(nqGrid, pwinput.structure.lattice.reciprocalBase())


__date__ = "$Mar 24, 2010 9:59:39 AM$"


    #    # XXX: Take 'asr' parameter from Q2R instead of setting it manually
#    def _asr(self, director):
#        return "'crystal'"


#        pwdir       = self._pwpath(director)
#        pwfile      = qeinput(director, self._inv.id, "PW")
#        pwpath      = packname(pwfile.id, ".in")
#        pwpath      = os.path.join(pwdir, pwpath)
#        pwInput     = PWInput(filename = pwpath)
#        pwInput.parse()

#        nl          = mdinput.namelist("input")
#        # Populate grid
#        nqGrid      = [int(nl.param("nk1")), int(nl.param("nk2")), int(nl.param("nk3"))]
        # XXX Handle case when parameters are not set
#        qpoints     = kmesh.kMeshCart(nqGrid, pwInput.structure.lattice.reciprocalBase())
#
#        return qpoints


#    def _pwpath(self, director):
#        # Example: pwdir   = "/home/dexity/exports/vnf/vnfb/content/data/tmp/tmpTRqFuy/8CNH5MUJ"
#        return resultsdir(director, self._inv.id, "PW")    # tmp results directory





#        method      = self._subtype()
#        if method == "dispersion":
#            qpoints = self._qpoints(self._director, matdynInput)
#            matdynInput.qpoints.set(qpoints)
#            # Add nk points?
#            nl  = matdynInput.namelists["input"]
#            nl.add("nk1", self.nk1)
#            nl.add("nk2", self.nk2)
#            nl.add("nk3", self.nk3)
#



#    def _subtype(self):
#        "Returns subtype of simulation: 'dos' or 'dispersion'"
#        methods     = MATDYN_METHOD.keys()
##        option      = int(self._inv.method)
#        return methods[int(self._subtype)]
#

#    def _matdynInput(self):
#        "Returns input object that can be later on used to add parameters"
#        # E.g.: /home/dexity/espresso/qejobs/643E2QQI/default.fc
#        q2rresult  = Q2RResult(self._director, self._inv.id)
#
#        self._input   = MatdynInput()
#        nl      = Namelist("input")
#        self._input.addNamelist(nl)
#        nl.add("asr",   q2rresult.zasr())   #self._asr(director)
#        nl.add("flfrc", q2rresult.flfrc())   #"'%s'" % path
#        nl.add("dos",   DOS)
#        nl.add("nk1",   self._inv.nk1)
#        nl.add("nk2",   self._inv.nk2)
#        nl.add("nk3",   self._inv.nk3)
#
##        # Add amasses
##        list    = self._amasses(self._director)
##        for m in list:
##            nl.add(m[0], m[1])
#
#        return self._input

#    # Copied from generate-phr.py
#    def _amasses(self, director):
#        """Returns list of tuples with amass label and mass value from PW input configuration
#        Example: [("amass(1)", "35.5"), ("amass(2)", "54.3")]
#        """
#        list    = []    # amass list
#        masses  = self._masses(director)
#        for l in range(len(masses)):
#            list.append(("amass(%s)" % str(l+1), masses[l][1]))
#
#        return list
#
#
#
#    # Copied from generate-q2r.py
#    def _masses(self, director):
#        # PW configuration input
#        pwinput     = inputRecord(director, self.inventory.id, "PW")
#        fname       = defaultInputName(pwinput.type)
#        text        = readRecordFile(director.dds, pwinput, fname)
#        pw          = QEInput(config = text)
#        pw.parse()
#
#        list        = []
#        # List of atom of format: [('Ni', '52.98', 'Ni.pbe-nd-rrkjus.UPF'), (...)]
#        atoms       = pw.structure()
#        for a in atoms:
#            list.append((a[0], a[1]))
#
#        return list

