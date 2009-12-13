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

# Update column from QECalc

class QESetting(QETable):

    name = "qesettings"
    import dsaw.db

    simulationid    = dsaw.db.varchar(name="simulationid", length=8)
    simulationid.constraints = 'REFERENCES qesimulations (id)'    # Important
    simulationid.meta['tip'] = "Task id"

    # Later on can be tranformed to a separate File table
    sname    = dsaw.db.varchar(name="sname", length=1024, default='')
    sname.meta['tip'] = "Filename assiciated with this configuration"

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = "description"

    numproc     = dsaw.db.integer(name='numproc', default = 0)
    numproc.meta['tip'] = "Number of processes to occupy"

    numnodes    = dsaw.db.integer(name='numnodes', default = 0)
    numnodes.meta['tip'] = "Number of nodes"

    # Should be moved Server???
    procpernode = dsaw.db.integer(name='procpernode', default = 0)
    procpernode.meta['tip'] = "Number of processes per node"
    
    npool       = dsaw.db.integer(name='npool', default = 0)
    npool.meta['tip'] = "Parameters npool"

    executable  = dsaw.db.varchar(name='executable', length=512, default='')
    executable.meta['tip'] = "Name of executable"

    params      = dsaw.db.varchar(name='params', length=512, default='')
    params.meta['tip'] = "Arbitrary parameters"

    modules     = dsaw.db.varchar(name='modules', length=512, default='')
    modules.meta['tip'] = "Modules"

    timecreated = dsaw.db.varchar(name="timecreated", length=16, default='')
    timecreated.meta['tip'] = "Time Created"

    timemodified = dsaw.db.varchar(name="timemodified", length=16, default='')
    timemodified.meta['tip'] = "Time Modified"

    # Keep it just in case
    text = dsaw.db.varchar(name="text", length=8192, default='')
    text.meta['tip'] = "text"


__date__ = "$Dec 10, 2009 10:08:22 PM$"


