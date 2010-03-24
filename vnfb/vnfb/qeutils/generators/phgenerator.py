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
#from vnfb.qeutils.qeutils import inputRecord, readRecordFile, defaultInputName
from vnfb.qeutils.results.resultpath import ResultPath

TR2_PH  = "1.0d-16"
LDISP   = ".true."

class PHGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._simtype   = inventory.simtype     # Special case

    # XXX:  Handle prefix properly (should be same as in pw input)
    def inputph(self):
        input      = QEInput(type='ph')
        input.header = "phonon simulation\n"
        nl  = Namelist("inputph")
        nl.add("nq1", self._inv.nq1)
        nl.add("nq2", self._inv.nq2)
        nl.add("nq3", self._inv.nq3)
        nl.add("tr2_ph", TR2_PH)
        nl.add("ldisp", LDISP)
        #nl.add("prefix", QE_PREFIX)    

        # Add amasses
        list    = self._amasses()
        for m in list:
            nl.add(m[0], m[1])

        input.addNamelist(nl)
        return input.toString()


    def _amasses(self):
        """Returns list of tuples with amass label and mass value from PW input configuration
        Example: [("amass(1)", "35.5"), ("amass(2)", "54.3")]
        """
        list    = []    # amass list
        masses  = self._masses()
        for l in range(len(masses)):
            list.append(("amass(%s)" % str(l+1), masses[l][1]))

        return list


    # XXX: Doesn't handle error when PW input file is not properly written (e.g. "atomic_species" is missing)
    def _masses(self):
        # PW configuration input
        resultpath  = ResultPath(self._director, simid, type)
        fname       = resultpath.resultFiles("input")
        try:
            text    = open(fname).read()    # Try read the file
        except:
            return None     # File not read, no masses list returned
#        pwinput     = inputRecord(director, self.inventory.id, "PW")
#        fname       = defaultInputName(pwinput.type)
#        text        = readRecordFile(director.dds, pwinput, fname)
        pw          = QEInput(config = text)
        pw.parse()

        list        = []
        # List of atom of format: [('Ni', '52.98', 'Ni.pbe-nd-rrkjus.UPF'), (...)]
        atoms       = pw.structure()
        for a in atoms:
            list.append((a[0], a[1]))

        return list


__date__ = "$Mar 24, 2010 9:59:39 AM$"


