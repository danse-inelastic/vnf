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
QESimulation - table that holds data for sequence (or chain) of Quantum Espresso
simulation steps (e.g. PW, PH)
    Total Energy:               PW
    Electron DOS:               PW -> DOS
    Electron Dispersion:        PW -> DOS
    Geometry Optimization:      PW
    Single-Phonon:              PW -> PH -> DYNMAT
    Multi-Phonon DOS:           PW -> PH -> Q2R -> MATDYN
    Multi-Phonon Dispersion:    PW -> PH -> Q2R -> MATDYN

Notes:
    - It has a bit different meaning from other "simulation" or "computation" tables used
in VNF (e.g. gulpsimulations or bvkcomputations) which refer to the actual simulation steps.
    - This table is Quantum Espresso specific
    - Has 'creator' field (owned table)
"""

from vnfb.utils.qeconst import SIMULATIONS, LABELS
from vnfb.components.QETable import QETable as base

class QESimulation(base):

    name = "qesimulations"
    import dsaw.db

    id = dsaw.db.varchar(name="id", length=8)
    id.constraints = 'PRIMARY KEY'
    id.meta['tip'] = "the unique id"

    sname = dsaw.db.varchar(name="sname", length=128, default='')
    sname.meta['tip'] = ""

    creator = dsaw.db.varchar(name="creator", length=128, default='')
    creator.meta['tip'] = ""

    package = dsaw.db.varchar(name="package", length=128, default='')
    package.meta['tip'] = ""

    type = dsaw.db.varchar(name="type", length=128, default='')
    type.meta['tip'] = ""

    description = dsaw.db.varchar(name="description", length=1024, default='')
    description.meta['tip'] = ""

    formula = dsaw.db.varchar(name="formula", length=32, default='')
    formula.meta['tip'] = ""

    timeCreated = dsaw.db.varchar(name="timeCreated", length=16, default='')
    timeCreated.meta['tip'] = "timeCreated"

    timeModified = dsaw.db.varchar(name="timeModified", length=16, default='')
    timeModified.meta['tip'] = "timeModified"

    label       = dsaw.db.varchar(name="label", length=128, default='')
    label.meta['tip'] = "So far label can be 'Favorite' or 'Example' only"


# Default records
defaults    = ({"id": 1, "sname": 'MgB2_SP', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[4], "description": 'Single-Phonon simualtion',
                "formula": 'MgB2', "label": LABELS["F"]},
                {"id": 2, "sname": 'MgB2_E', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[0], "description": 'Electron simualtion',
                "formula": 'MgB2', "label": LABELS["F"]},
                {"id": 3, "sname": 'MgB2_MP', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[5], "description": 'Multy-Phonon simualtion',
                "formula": 'MgB2', "label": LABELS["F"]},
                {"id": 4, "sname": 'Ni_Energy', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[0], "description": 'Total Energy simualtion',
                "formula": 'Ni', "label": LABELS["E"]},
                {"id": 5, "sname": 'Ni_E_DOS', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[1], "description": 'Electron DOS simualtion',
                "formula": 'Ni', "label": LABELS["E"]},
                {"id": 6, "sname": 'Ni_Ph_DOS', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[5], "description": 'Multy-Phonon DOS simualtion',
                "formula": 'Ni', "label": LABELS["E"]})

# Init tables
def inittable(clerk):
    for params in defaults:
        r   = QESimulation()
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



# **************** DEAD CODE ***********************************



#    isFavorite = dsaw.db.boolean(name="isFavorite", default=True)   #?
#    isFavorite.meta['tip'] = ""
#
#    isExample = dsaw.db.boolean(name="isExample", default=False)
#    isExample.meta['tip'] = ""



#import dsaw.db
#from vnf.dom.MaterialSimulation import MaterialSimulation as base
#
#class QESimulation(base):
#
#    name    = 'qesimulations'
#    matter  = dsaw.db.versatileReference(name='matter')
#    type    = dsaw.db.varchar(name='type', length = 128)

# id, date, creator, short_description, globalpointer, results_state, job, matter, type

__date__ = "$Nov 22, 2009 11:42:42 PM$"


