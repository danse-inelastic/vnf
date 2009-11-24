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

# type   = ("Total Energy",
#           "Electron DOS",
#           "Electron Dispersion",
#           "Geometry Optimization",
#           "Single-Phonon",
#           "Multi-Phonon DOS",
#           "Multi-Phonon Dispersion")

import dsaw.db
from vnf.dom.MaterialSimulation import MaterialSimulation as base

class QESimulation(base):

    name    = 'qesimulations'
    matter  = dsaw.db.versatileReference(name='matter')
    type    = dsaw.db.varchar(name='type', length = 128)

# id, date, creator, short_description, globalpointer, results_state, job, matter, type

__date__ = "$Nov 22, 2009 11:42:42 PM$"


