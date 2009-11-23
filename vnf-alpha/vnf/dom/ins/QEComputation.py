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
from MaterialModeling import MaterialModeling as base

class QEComputation(base):

    name    = 'qecomputations'
    matter  = dsaw.db.versatileReference(name='matter')
    type    = dsaw.db.varchar(name='type', length = 128)

__date__ = "$Nov 22, 2009 11:42:42 PM$"


