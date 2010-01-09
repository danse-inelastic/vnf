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
#from vnfb.dom.Computation import Computation
from vnfb.dom.MaterialSimulation import MaterialSimulation

#from dsaw.model.Inventory import Inventory as InvBase

from memd.gulp.GulpSettings import GulpSettings
GulpSettingsHolder = o2t(GulpSettings, {'subclassFrom': MaterialSimulation, 'dbtablename':'gulpsettings'})
GulpSettingsHolder.job_builder = 'material_simulations/gulpSettings'
GulpSettingsHolder.actor = 'material_simulations/gulpSettings'
GulpSettingsHolder.result_retriever = 'material_simulations/gulpSettings'




# version
__id__ = "$Id$"

# End of file 
