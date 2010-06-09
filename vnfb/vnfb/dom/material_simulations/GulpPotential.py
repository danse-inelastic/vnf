# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#

from _ import o2t

from memd.gulp.GulpPotential import GulpPotential as GulpPotentialBase
GulpPotential = o2t(GulpPotentialBase)

#import dsaw.db
#GulpSettings.addColumn(
#    dsaw.db.reference(name='matter', table=Structure, backref='gulpsettings')
#    )


# version
__id__ = "$Id$"

# End of file 