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

# still import from vnf-alpha dom. need to change
#from vnfb.dom.Computable import Computable
from vnfb.dom.Computation import Computation
from vnfb.dom.AtomicStructure import Structure
#from vnfb.dom.MaterialSimulation import MaterialSimulation

#from dsaw.model.Inventory import Inventory as InvBase

from memd.gulp.GulpSettings import GulpSettings as GulpSettingsDO
GulpSettings = o2t(GulpSettingsDO, {'subclassFrom': Computation, 'dbtablename':'gulpsettings'})
GulpSettings.job_builder = 'material_simulations/gulpSettings'
GulpSettings.actor = 'material_simulations/gulpSettings'
GulpSettings.result_retriever = 'material_simulations/gulpSettings'

#import dsaw.db
#GulpSettings.addColumn(
#    dsaw.db.reference(name='matter', table=Structure, backref='gulpsettings')
#    )


# version
__id__ = "$Id$"

# End of file 
