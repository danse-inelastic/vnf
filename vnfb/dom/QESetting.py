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
QESetting - table that holds simulation settings

Notes:
     - Settings are specific for QE simulations, make general?

"""

from vnfb.components.QETable import QETable
from vnfb.qeutils.qeconst import SETTINGS

# Update column from QECalc

class QESetting(QETable):

    name = "qesettings"
    import dsaw.db

    # Should refer to qetasks? Yes, eventually! Keep it here for now
    simulationid    = dsaw.db.varchar(name="simulationid", length=64)
    simulationid.constraints = 'REFERENCES qesimulations (id)'    # Important
    simulationid.meta['tip'] = "Simulation id"

    serverid    = dsaw.db.varchar(name="serverid", length=64)
    serverid.constraints = 'REFERENCES servers (id)'    # Important
    serverid.meta['tip'] = "Default server for the simulation"

    # Later on can be tranformed to a separate File table
    sname    = dsaw.db.varchar(name="sname", length=1024, default='')
    sname.meta['tip'] = "Filename assiciated with this configuration"

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = "description"

    numproc     = dsaw.db.integer(name='numproc', default = SETTINGS["numproc"])
    numproc.meta['tip'] = "Number of processes to occupy"

    numnodes    = dsaw.db.integer(name='numnodes', default = SETTINGS["numnodes"])
    numnodes.meta['tip'] = "Number of nodes"

    npool       = dsaw.db.integer(name='npool', default = SETTINGS["npool"])
    npool.meta['tip'] = "Parameters npool"

    executable  = dsaw.db.varchar(name='executable', length=512, default = SETTINGS["executable"])
    executable.meta['tip'] = "Name of executable"

    params      = dsaw.db.varchar(name='params', length=512, default='')
    params.meta['tip'] = "Arbitrary parameters"

    modules     = dsaw.db.varchar(name='modules', length=512, default = SETTINGS["modules"])
    modules.meta['tip'] = "Modules"

    timecreated = dsaw.db.varchar(name="timecreated", length=32, default='')
    timecreated.meta['tip'] = "Time Created"

    timemodified = dsaw.db.varchar(name="timemodified", length=32, default='')
    timemodified.meta['tip'] = "Time Modified"

    # Keep it just in case
    text = dsaw.db.varchar(name="text", length=8192, default='')
    text.meta['tip'] = "text"

    optlevel    = dsaw.db.integer(name='optlevel', default = 0)
    optlevel.meta['tip'] = "Optimization level. Definition depends on the cluster. 0 - no optimization"



__date__ = "$Dec 10, 2009 10:08:22 PM$"


