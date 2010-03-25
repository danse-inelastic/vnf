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

"""
Generates PH configuration file from scratch
"""
from vnfb.qeutils.qeparser.qeinput import QEInput
from vnfb.qeutils.qeparser.namelist import Namelist
from vnfb.qeutils.results.pwresult import PWResult

TR2_PH  = "1.0d-12"
LDISP   = ".true."

class PHGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None

    # XXX:  Handle prefix properly (should be same as in pw input)
    def setInputph(self):
        self._input      = QEInput(type='ph')
        self._input.header = "phonon simulation\n"
        nl  = Namelist("inputph")
        self._input.addNamelist(nl)
        
        nl.add("nq1",       self._inv.nq1)
        nl.add("nq2",       self._inv.nq2)
        nl.add("nq3",       self._inv.nq3)
        nl.add("tr2_ph",    TR2_PH)
        nl.add("ldisp",     LDISP)
        #nl.add("prefix",   QE_PREFIX)
        self._addAmasses(nl)


    def toString(self):
        if not self._input:
            return ""
        
        return self._input.toString()


    def amasses(self):
        """Returns list of tuples with amass label and mass value from PW input configuration
        Example: [("amass(1)", "35.5"), ("amass(2)", "54.3")]
        """
        pwresult    = PWResult(self._director, self._inv.id)
        species     = pwresult.species()    # Example: masses = [("Al", "29.7"), ("Ni", "56.7") ...]
        if not species:
            return None # No masses, no amasses :)
        
        list    = []    # amass list
        for l in range(len(species)):
            list.append(("amass(%s)" % str(l+1), species[l][1]))

        return list


    def _addAmasses(self, nl):
        "Takes namelist and adds amasses"
        masses    = self.amasses()

        if not masses:  # In case if not masses are found in PW input
            nl.add("amass", "ERROR: masses not defined in PW input file!")
            return

        for m in masses:
            nl.add(m[0], m[1])
        


__date__ = "$Mar 24, 2010 9:59:39 AM$"


