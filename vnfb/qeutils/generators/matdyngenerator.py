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

from vnf.qeutils.results.q2rresult import Q2RResult
from vnf.qeutils.qeconst import MATDYN_METHOD_LIST
from vnf.qeutils.qeparser.namelist import Namelist
from vnf.qeutils.results.pwresult import PWResult
from vnf.qeutils.generators.phgenerator import PHGenerator

from qecalc.qetask.qeparser.matdyninput import MatdynInput
from vnf.qeutils.qecalcutils import kmesh

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
        subtype  = int(self._inv.subtype) # 0, 1
        if not subtype in range(len(MATDYN_METHOD_LIST)):  # if out of range
            return

        self._subtype   = MATDYN_METHOD_LIST[subtype]


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


    def flfrc(self):
        "Returns flfrc parameter from Q2R results"
        q2rresult       = Q2RResult(self._director, self._inv.id)
        return q2rresult.flfrc()


    def toString(self):
        return self._input.toString()


    def _qpoints(self):
        "Returns qpoints"
        nqGrid      = [int(self._inv.nk1), int(self._inv.nk2), int(self._inv.nk3)]

        pwresult    = PWResult(self._director, self._inv.id)        
        pwinput     = pwresult.input()
        return kmesh.kMeshCart(nqGrid, pwinput.structure.lattice.reciprocalBase())


__date__ = "$Mar 24, 2010 9:59:39 AM$"
