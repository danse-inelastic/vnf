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
QESimulationTask - table that keeps many-to-many relationship between QESimulation
and QETask tables

Notes:
    - None
"""

from vnfb.components.QETable import QETable

class QESimulationTask(QETable):
    
    name = "qesimulationtasks"
    import dsaw.db
    
    # TODO: Remove reference to QESimulation from QETask table first,
    #       then uncomment columns
    simulationid    = dsaw.db.varchar(name="simulationid", length=64)
    simulationid.constraints = 'REFERENCES qesimulations (id)'    # Important
    simulationid.meta['tip'] = "simulationid"
    
    taskid    = dsaw.db.varchar(name="taskid", length=64)
    taskid.constraints = 'REFERENCES qetasks (id)'    # Important
    taskid.meta['tip'] = "Task id"

__date__ = "$Dec 12, 2009 10:46:37 PM$"


