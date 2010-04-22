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
QEConvergenceTask - table that keeps many-to-many relationship between QEConvergence
and QETask tables

Notes:
    - None
"""

from vnfb.components.QETable import QETable

class QEConvergenceTask(QETable):

    name = "qeconvergencetasks"
    import dsaw.db

    convergenceid    = dsaw.db.varchar(name="convergenceid", length=64)
    convergenceid.constraints = 'REFERENCES qeconvergences (id)'    # Important
    convergenceid.meta['tip'] = "convergenceid"

    taskid    = dsaw.db.varchar(name="taskid", length=64)
    taskid.constraints = 'REFERENCES qetasks (id)'    # Important
    taskid.meta['tip'] = "Task id"


__date__ = "$Apr 22, 2010 12:25:44 PM$"


