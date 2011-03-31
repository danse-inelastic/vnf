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

from vnf.components.QETable import QETable

class QEJob(QETable):
    # 'name' attribute should be present in every class table.
    name = "qejobs"
    import dsaw.db

    taskid = dsaw.db.varchar(name="taskid", length=64)
    taskid.constraints = 'REFERENCES qetasks (id)'
    taskid.meta['tip'] = ""

    serverid    = dsaw.db.varchar(name="serverid", length=64)
    serverid.constraints = 'REFERENCES servers (id)'
    serverid.meta['tip'] = ""

    creator = dsaw.db.varchar(name="creator", length=128, default='')
    creator.meta['tip'] = ""

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = ""

    status = dsaw.db.varchar(name="status", length=64, default='')
    status.meta['tip'] = ""

    timesubmitted = dsaw.db.varchar(name="timesubmitted", length=32, default='')
    timesubmitted.meta['tip'] = "timesubmitted"

    timestarted = dsaw.db.varchar(name="timestarted", length=32, default='')
    timestarted.meta['tip'] = "timestarted"

    timerestarted = dsaw.db.varchar(name="timerestarted", length=32, default='')
    timerestarted.meta['tip'] = "timerestarted"

    timecompleted = dsaw.db.varchar(name="timecompleted", length=32, default='')
    timecompleted.meta['tip'] = "timecompleted"

    exitcode = dsaw.db.integer(name="exitcode", default=-1)
    exitcode.meta['tip'] = "exitcode"

    numberprocessors = dsaw.db.integer(name="numberprocessors", default=0)
    numberprocessors.meta['tip'] = "numberprocessors"

    errorfilename = dsaw.db.varchar(name="errorfilename", length=256, default='STDERR.log')
    errorfilename.meta['tip'] = "errorfilename"

    outputfilename = dsaw.db.varchar(name="outputfilename", length=256, default='STDOUT.log')
    outputfilename.meta['tip'] = "outputfilename"

    statusmessage = dsaw.db.varchar(name="statusmessage", length=256, default='')
    statusmessage.meta['tip'] = "statusmessage"


# Default records
defaults    = ({})

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


