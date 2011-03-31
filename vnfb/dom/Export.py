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
Export  - keeps records about performed exports

Notes:
    - This is a preliminary interface which can be changed depending on existing problems
    - Set reference to ExportSimulation table?
"""

from vnf.components.QETable import QETable

class Export(QETable):
    name = "exports"
    import dsaw.db

    short_description = dsaw.db.varchar(name="short_description", length=1024, default='')
    short_description.meta['tip'] = ""

    # in MS
    timecreated = dsaw.db.varchar(name="timecreated", length=16, default='')
    timecreated.meta['tip'] = "timecreated"


__date__ = "$Mar 31, 2010 1:24:40 PM$"


