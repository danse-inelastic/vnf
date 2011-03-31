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

class QEConvParam(QETable):
    name = "qeconvparams"
    import dsaw.db

    convergenceid    = dsaw.db.varchar(name="convergenceid", length=64)
    convergenceid.constraints = 'REFERENCES qeconvergences (id)'    # Important
    convergenceid.meta['tip'] = "Convergence id"

    pname = dsaw.db.varchar(name="pname", length=128, default='')
    pname.meta['tip'] = "Parameter name"

    tolerance   = dsaw.db.real(name="tolerance", default=1.0)
    tolerance.meta['tip'] = "Error in percents"

    maxsteps    = dsaw.db.integer(name="maxsteps", default=2)
    maxsteps.meta['tip'] = "Max number of steps"

    value       = dsaw.db.varchar(name="value", length=512, default='')
    value.meta['tip'] = "Current value of the parameter"

    optimal     = dsaw.db.varchar(name="optimal", length=512, default='')
    optimal.meta['tip'] = "Optimal value"

    type        = dsaw.db.varchar(name="type", length=64, default='')
    type.meta['tip'] = "Type of parameter: int, double, vector"

    startvalue  = dsaw.db.varchar(name="startvalue", length=512, default='')
    startvalue.meta['tip'] = "Starting value of the parameter. Handles int, double and vector (e.g. [a, b, c])"

    step  = dsaw.db.varchar(name="step", length=512, default='')
    step.meta['tip'] = "Step of parameter. Handles int, double and vector"

    timecreated = dsaw.db.varchar(name="timecreated", length=32, default='')
    timecreated.meta['tip'] = "timecreated"

    timemodified = dsaw.db.varchar(name="timemodified", length=32, default='')
    timemodified.meta['tip'] = "timemodified"

__date__ = "$Apr 21, 2010 6:02:30 PM$"


