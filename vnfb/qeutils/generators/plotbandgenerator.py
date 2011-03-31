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

from vnf.qeutils.results.pwresult import PWResult
from vnf.qeutils.results.bandsresult import BANDSResult
from vnf.qeutils.results.resultpath import PSBAND, XMGRBAND


class PLOTBANDGenerator(object):

    def __init__(self, director, inventory):
        self._director  = director
        self._inv       = inventory
        self._input     = []    # Input lines
        self._init()


    def _init(self):
        "Additional init"
        self._bandsresult   = BANDSResult(self._director, self._inv.id)
        self._pwresult      = PWResult(self._director, self._inv.id, linkorder = 1)


    def setInput(self):
        bandsdat    = self._bandsresult.bandsFile() # 
        efermi      = self._pwresult.fermiEnergy()  # Example: (8.3457, 'eV')
        efermi      = efermi[0]
        self._input.append(bandsdat)
        self._input.append("%f %f" % (self._inv.emin, self._inv.emax))
        self._input.append(XMGRBAND)
        self._input.append(PSBAND)
        self._input.append("%f" % efermi)
        self._input.append("%f %f" % (self._inv.deltae, efermi) )


    def toString(self):
        return "\n".join(self._input)


__date__ = "$Mar 24, 2010 9:59:39 AM$"


