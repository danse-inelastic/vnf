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

class QEConvParamTask(QETable):

    name = "qeconvparamtasks"
    import dsaw.db

    convparamid    = dsaw.db.varchar(name="convparamid", length=64)
    convparamid.constraints = 'REFERENCES qeconvparams (id)'    # Important
    convparamid.meta['tip'] = "convparamid"

    taskid    = dsaw.db.varchar(name="taskid", length=64)
    taskid.constraints = 'REFERENCES qetasks (id)'    # Important
    taskid.meta['tip'] = "Task id"


__date__ = "$Apr 22, 2010 12:25:44 PM$"


