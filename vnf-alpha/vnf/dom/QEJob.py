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
QEJob - table that holds jobs data for Quantum Espresso simulations

Notes:
    - Has 'creator' field (owned table)
"""

from vnf.dom.QESimulation import QESimulation
from vnf.dom.Server import Server

from vnfb.utils.qeconst import STATES
from vnfb.utils.qeutils import timestamp
from dsaw.db.WithID import WithID

from vnfb.components.QETable import QETable as base

class QEJob(base, WithID):
    # 'name' attribute should be present in every class table.
    name = "qejobs"
    import dsaw.db

#    id          = dsaw.db.varchar(name="id", length=8)
#    id.constraints = 'PRIMARY KEY'
#    id.meta['tip'] = "the unique id"

    simulationId = dsaw.db.reference(name='simulationId', table=QESimulation) #varchar(name="simulationId", length=8)
    simulationId.meta['tip'] = ""

    creator = dsaw.db.varchar(name="creator", length=128, default='')
    creator.meta['tip'] = ""

    serverId    = dsaw.db.reference(name='serverId', table=Server)
    serverId.meta['tip'] = ""

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = ""

    status = dsaw.db.varchar(name="status", length=64, default='')
    status.meta['tip'] = ""

    timeSubmitted = dsaw.db.varchar(name="timeSubmitted", length=16, default='')
    timeSubmitted.meta['tip'] = "timeSubmitted"

    timeStarted = dsaw.db.varchar(name="timeStarted", length=16, default='')
    timeStarted.meta['tip'] = "timeStarted"

    timeRestarted = dsaw.db.varchar(name="timeRestarted", length=16, default='')
    timeRestarted.meta['tip'] = "timeRestarted"

    timeCompleted = dsaw.db.varchar(name="timeCompleted", length=16, default='')
    timeCompleted.meta['tip'] = "timeCompleted"

    exitCode = dsaw.db.integer(name="exitCode", default=-1)
    exitCode.meta['tip'] = "exitCode"

    numberProcessors = dsaw.db.integer(name="numberProcessors", default=0)
    numberProcessors.meta['tip'] = "numberProcessors"

    errorFilename = dsaw.db.varchar(name="errorFilename", length=256, default='stderr.log')
    errorFilename.meta['tip'] = "errorFilename"

    outputFilename = dsaw.db.varchar(name="outputFilename", length=256, default='stdout.log')
    outputFilename.meta['tip'] = "outputFilename"

    statusMessage = dsaw.db.varchar(name="statusMessage", length=256, default='')
    statusMessage.meta['tip'] = "statusMessage"


# Default records
defaults    = ({"id": 1, "creator": "dexity", "simulationId": 4, "serverId": 1,
               "status": STATES["C"], "timeCompleted": timestamp() + 60, "exitCode": 0,
                "numberProcessors": 8},
               {"id": 2, "creator": "dexity", "simulationId": 5, "serverId": 1,
               "status": STATES["C"], "timeCompleted": timestamp() + 60, "exitCode": 0,
                "numberProcessors": 8},
               {"id": 3, "creator": "dexity", "simulationId": 6, "serverId": 1,
               "status": STATES["R"], "timeCompleted": timestamp() + 60, "exitCode": 0,
                "numberProcessors": 8})

# Init tables
def inittable(clerk):
    for params in defaults:
        r   = QEJob()
        r.setClerk(clerk)
        r.createRecord(params)


def test():
    for e in defaults:
        s = ""
        for v in e.keys():
            s += "%s: %s " % (v, e[v])
        print s

if __name__ == "__main__":
    test()

__date__ = "$Nov 24, 2009 5:49:39 PM$"


