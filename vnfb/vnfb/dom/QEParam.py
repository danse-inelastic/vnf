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
QEParams - table for configuration parameters used in convergence tests
"""

from vnfb.components.QETable import QETable

class QEParam(QETable):
    name = "qeparams"
    import dsaw.db

#    simulationid    = dsaw.db.varchar(name="simulationid", length=64)
#    simulationid.constraints = 'REFERENCES qesimulations (id)'    # Important
#    simulationid.meta['tip'] = "Simulation id"
#
#    tolerance = 1, nMaxSteps

__date__ = "$Apr 21, 2010 6:02:30 PM$"


