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
QETask - table that holds data for simgle Quantum Espresso simulation step. Currently
         the following types are supported:
            pw, ph, dos, q2r, dynmat, matdyn

Notes:
    - It has similar meaning to "simulation" or "computation" tables used in VNF
    (e.g. gulpsimulations or bvkcomputations)
    - This table is Quantum Espresso specific
"""

from vnfb.utils.qeconst import SIMULATIONS
from vnfb.components.QETable import QETable

from MaterialSimulation import MaterialSimulation

# WithID -> id

class QETask(QETable):

    name = "qetasks"
    import dsaw.db

    # in MS
    short_description = dsaw.db.varchar(name="short_description", length=1024, default='')
    short_description.meta['tip'] = ""

    # in MS
    date = dsaw.db.varchar(name="date", length=16, default='')
    date.meta['tip'] = "timecreated"

    # ?
    package = dsaw.db.varchar(name="package", length=128, default='Quantum Espresso')
    package.meta['tip'] = ""

    type = dsaw.db.varchar(name="type", length=128, default='')
    type.meta['tip'] = "Type of simulation task"

    timemodified = dsaw.db.varchar(name="timemodified", length=16, default='')
    timemodified.meta['tip'] = "timemodified"

    # ?
    label       = dsaw.db.varchar(name="label", length=128, default='Favorite')
    label.meta['tip'] = "Label associated with the simulation"

    # ???
    matter = dsaw.db.varchar(name="matter", length=128, default='')
    matter.meta['tip']  = "STUB"


# Default records
defaults    = ({},)

# Init tables
def inittable(clerk):
    for params in defaults:
        r   = QETask()
        r.setClerk(clerk)
        r.createRecord(params)


def test():
    for e in examples:
        s = ""
        for v in e:
            s += "%s " % v
        print s

if __name__ == "__main__":
    test()


__date__ = "$Dec 9, 2009 2:19:07 PM$"


