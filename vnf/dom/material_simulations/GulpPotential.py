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

from memdf.gulp.GulpPotential import GulpPotential
GulpPotentialTable = o2t(GulpPotential)

#import dsaw.db
#GulpSettings.addColumn(
#    dsaw.db.reference(name='matter', table=Structure, backref='gulpsettings')
#    )


# version
__id__ = "$Id$"

# End of file 
