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

from vnfb.components.QETable import QETable as base

class QEJob(base):
    # 'name' attribute should be present in every class table.
    name = "qejobs"
    import pyre.db

    id          = pyre.db.varchar(name="id", length=8)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    task = pyre.db.varchar(name="taskid", length=8)
    task.constraints = 'REFERENCES qetasks (id)'
    task.meta['tip'] = ""

    creator = pyre.db.varchar(name="creator", length=128, default='')
    creator.meta['tip'] = ""

    serverid    = pyre.db.varchar(name="serverid", length=8)
    serverid.constraints = 'REFERENCES servers (id)'
    serverid.meta['tip'] = ""

    description = pyre.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = ""

    status = pyre.db.varchar(name="status", length=64, default='')
    status.meta['tip'] = ""

    timesubmitted = pyre.db.varchar(name="timesubmitted", length=16, default='')
    timesubmitted.meta['tip'] = "timesubmitted"

    timestarted = pyre.db.varchar(name="timestarted", length=16, default='')
    timestarted.meta['tip'] = "timestarted"

    timerestarted = pyre.db.varchar(name="timerestarted", length=16, default='')
    timerestarted.meta['tip'] = "timerestarted"

    timecompleted = pyre.db.varchar(name="timecompleted", length=16, default='')
    timecompleted.meta['tip'] = "timecompleted"

    exitcode = pyre.db.integer(name="exitcode", default=-1)
    exitcode.meta['tip'] = "exitcode"

    numberprocessors = pyre.db.integer(name="numberprocessors", default=0)
    numberprocessors.meta['tip'] = "numberprocessors"

    errorfilename = pyre.db.varchar(name="errorfilename", length=256, default='stderr.log')
    errorfilename.meta['tip'] = "errorfilename"

    outputfilename = pyre.db.varchar(name="outputfilename", length=256, default='stdout.log')
    outputfilename.meta['tip'] = "outputfilename"

    statusmessage = pyre.db.varchar(name="statusmessage", length=256, default='')
    statusmessage.meta['tip'] = "statusmessage"


# Default records
defaults    = ({"id": 1, "creator": "dexity", "taskid": 4, "serverid": 1,
               "status": STATES["C"], "timecompleted": timestamp() + 60, "exitcode": 0,
                "numberprocessors": 8},
               {"id": 2, "creator": "dexity", "taskid": 5, "serverid": 1,
               "status": STATES["C"], "timecompleted": timestamp() + 60, "exitcode": 0,
                "numberprocessors": 8},
               {"id": 3, "creator": "dexity", "taskid": 6, "serverid": 1,
               "status": STATES["R"], "timecompleted": timestamp() + 60, "exitcode": 0,
                "numberprocessors": 8})

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


