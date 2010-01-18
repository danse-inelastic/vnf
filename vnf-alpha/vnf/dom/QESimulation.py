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

from vnfb.utils.qeconst import SIMULATIONS
from vnfb.components.QETable import QETable
from vnfb.dom.Computation import Computation

from MaterialSimulation import MaterialSimulation

# WithID -> id

class QESimulation(QETable):    #, Computation): #):

    name = "qesimulations"
    import dsaw.db

    serverid    = dsaw.db.varchar(name="serverid", length=64)
    serverid.constraints = 'REFERENCES servers (id)'    # Important
    serverid.meta['tip'] = "Default server for the simulation"

    structureid    = dsaw.db.varchar(name="structureid", length=64)
    structureid.constraints = 'REFERENCES atomicstructures (id)'    # Important
    structureid.meta['tip'] = "Atomic structure"

    sname = dsaw.db.varchar(name="sname", length=128, default='')
    sname.meta['tip'] = "Simulation name"

    # in MS
    creator = dsaw.db.varchar(name="creator", length=128, default='')
    creator.meta['tip'] = "User name"

    # in MS
    short_description = dsaw.db.varchar(name="short_description", length=1024, default='')
    short_description.meta['tip'] = "Description of the simulation"

    # in MS
    date = dsaw.db.varchar(name="date", length=16, default='')
    date.meta['tip'] = "timecreated"

    package = dsaw.db.varchar(name="package", length=128, default='Quantum Espresso')
    package.meta['tip'] = ""

    type = dsaw.db.varchar(name="type", length=128, default='')
    type.meta['tip'] = ""

    timemodified = dsaw.db.varchar(name="timemodified", length=16, default='')
    timemodified.meta['tip'] = "timemodified"

    label       = dsaw.db.varchar(name="label", length=128, default='')
    label.meta['tip'] = "Label associated with the simulation"

    matter = dsaw.db.integer(name="matter", default=0)
    matter.meta['tip']  = "(STUB) Refers to atomic group. Kind of useless but must have"

    @classmethod
    def getActorName(cls):
        if hasattr(cls, 'actor'): return cls.actor
        return cls.__name__.lower()


# Default records
defaults    = ({"id": 1, "sname": 'MgB2_SP', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[4], "short_description": 'Single-Phonon simualtion'},
                {"id": 2, "sname": 'MgB2_E', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[0], "short_description": 'Electron simualtion'},
                {"id": 3, "sname": 'MgB2_MP', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[5], "short_description": 'Multy-Phonon simualtion'},
                {"id": 4, "sname": 'Ni_Energy', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[0], "short_description": 'Total Energy simualtion'},
                {"id": 5, "sname": 'Ni_E_DOS', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[1], "short_description": 'Electron DOS simualtion'},
                {"id": 6, "sname": 'Ni_Ph_DOS', "creator": "dexity", "package": 'Quantum Espresso',
                "type": SIMULATIONS[5], "short_description": 'Multy-Phonon DOS simualtion'})

# Init tables
def inittable(clerk):
    for params in defaults:
        r   = QESimulation()
        r.setClerk(clerk)
        r.createRecord(params)


def test():
    for e in defaults:
        s = ""
        for v in e:
            s += "%s " % v
        print s

if __name__ == "__main__":
    test()



# **************** DEAD CODE ***********************************


#    matter = dsaw.db.versatileReference(name='matter')
#    matter.meta['tip']  = "stub"

#    id = dsaw.db.varchar(name="id", length=8)
#    id.constraints = 'PRIMARY KEY'
#    id.meta['tip'] = "the unique id"

#    creator = dsaw.db.varchar(name="creator", length=128, default='')
#    creator.meta['tip'] = ""

#    short_description = dsaw.db.varchar(name="short_description", length=1024, default='')
#    short_description.meta['tip'] = ""

#    formula = dsaw.db.varchar(name="formula", length=32, default='')
#    formula.meta['tip'] = ""

#    date = dsaw.db.varchar(name="date", length=16, default='')
#    date.meta['tip'] = "timeCreated"



#    from vnfb.utils.qeutils import stamp2date
#    timeCreated = dsaw.db.varchar(name="timeCreated", length=16, default='')
#    timeCreated.meta['tip'] = "timeCreated - replaced by 'date'"
#
#    description = dsaw.db.varchar(name="description", length=1024, default='')
#    description.meta['tip'] = "description - replaced by 'short_description'"




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


