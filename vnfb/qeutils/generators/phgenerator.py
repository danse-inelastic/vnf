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
from vnfb.qeutils.qeconst import SIMTYPE

TR2_PH      = "1.0d-12"
LDISP       = ".true."
EPSIL       = ".true."  # For isolators only
TRANS       = ".true."
LNSCF       = ".true."

class PHGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = None
        self._pwresult  = PWResult(self._director, self._inv.id)


    # XXX:  Handle prefix properly (should be same as in pw input)
    def setInputph(self):
        "Sets inputph depending on the simulation type"
        self._input      = QEInput(type='ph')
        self._input.header = "phonon simulation\n"
        nl  = Namelist("inputph")
        self._input.addNamelist(nl)
        
        self._simtype   = self._simtype()
        if not self._simtype:   # no simtype, no inputph population
            return

        if self._simtype == SIMTYPE["multiple-phonon"]:
            self._multiPhonInput()    # population of inputph for multiple phonon

        elif self._simtype == SIMTYPE["single-phonon"]:
            self._singlePhonInput()     # population of inputph for single phonon
            

    def toString(self):
        if not self._input:
            return ""
        
        return self._input.toString()


    def amasses(self):
        """Returns list of tuples with amass label and mass value from PW input configuration
        Example: [("amass(1)", "35.5"), ("amass(2)", "54.3")]
        """
        species     = self._pwresult.species()    # Example: masses = [("Al", "29.7"), ("Ni", "56.7") ...]
        if not species:
            return None # No masses, no amasses :)
        
        list    = []    # amass list
        for l in range(len(species)):
            list.append(("amass(%s)" % str(l+1), species[l][1]))

        return list


    def isGammaPoint(self):
        "Checks if phonon point is gamma point"
        # Rudimentary filter
        if self._inv.kx == '' or self._inv.ky == '' or self._inv.kz == '':
            return False

        return float(self._inv.kx) == 0.0 and float(self._inv.ky) == 0.0 and float(self._inv.kz) == 0.0


    # XXX: Reset parameters 'prefix', 'outdir', 'fildyn'
    def _singlePhonInput(self):
        "Takes namelist and populates inputph for single phonon"
        nl  = self._input.namelist("inputph")
        nl.add("tr2_ph",    TR2_PH)
        nl.add("trans",    TRANS)
        self._addAmasses(nl)
        self._addEpsil(nl)  # for isolator only
        self._addLnscf(nl)  # for non-Gamma point
        self._input.addAttach("%s %s %s" % (self._inv.kx, self._inv.ky, self._inv.kz))


    def _multiPhonInput(self):
        "Takes namelist and populates inputph for multiple phonons"
        nl  = self._input.namelist("inputph")
        nl.add("nq1",       self._inv.nq1)
        nl.add("nq2",       self._inv.nq2)
        nl.add("nq3",       self._inv.nq3)
        nl.add("tr2_ph",    TR2_PH)
        nl.add("ldisp",     LDISP)
        #nl.add("prefix",   QE_PREFIX)
        self._addAmasses(nl)
        self._addEpsil(nl)  # for isolator only


    def _addAmasses(self, nl):
        "Takes namelist and adds amasses"
        masses    = self.amasses()

        if not masses:  # In case if not masses are found in PW input
            nl.add("amass", "ERROR: masses not defined in PW input file!")
            return

        for m in masses:
            nl.add(m[0], m[1])


    def _addLnscf(self, nl):
        "Adds 'lnscf' parameter for non-Gamma point"
        if not self.isGammaPoint():
            nl.add("lnscf", LNSCF)


    def _addEpsil(self, nl):
        "Add 'epsil' parameter for isolators only. Do nothing otherwise"
        if self._pwresult.isIsolator():
            nl.add("epsil", EPSIL)

        
    def _simtype(self):
        "Be cautious in case if inventory doesn't have simtype"
        try:
            simtype   = self._inv.simtype
        except AttributeError:
            return None

        return simtype



__date__ = "$Mar 24, 2010 9:59:39 AM$"
