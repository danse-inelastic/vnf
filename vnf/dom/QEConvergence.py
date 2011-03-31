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
Convergence - table that stores records for convergence tests
"""


from vnf.components.QETable import QETable

class QEConvergence(QETable):
    name = "qeconvergences"
    import dsaw.db

    simulationid    = dsaw.db.varchar(name="simulationid", length=64)
    simulationid.constraints = 'REFERENCES qesimulations (id)'    # Important
    simulationid.meta['tip'] = "Simulation id"

    cname = dsaw.db.varchar(name="cname", length=128, default='')
    cname.meta['tip'] = "Convergence test name"

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = "Description of the convergence test"

    timecreated = dsaw.db.varchar(name="timecreated", length=32, default='')
    timecreated.meta['tip'] = "timecreated"

    type = dsaw.db.varchar(name="type", length=128, default='')
    type.meta['tip'] = "Convergence type (criteria): 'total-energy', 'frequency', later 'fermi-energy'"

    timemodified = dsaw.db.varchar(name="timemodified", length=32, default='')
    timemodified.meta['tip'] = "timemodified"

    label       = dsaw.db.varchar(name="label", length=128, default='')
    label.meta['tip'] = "Label associated with the simulation"

    progress    = dsaw.db.varchar(name="progress", length=128, default='')
    progress.meta['tip'] = "Current job id "


__date__ = "$Apr 21, 2010 5:23:35 PM$"


