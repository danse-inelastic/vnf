

from _ import o2t

from vnf.dom.Computation import Computation

from memd.gulp.GulpSettings import GulpSettings as GulpSettingsDO
GulpSettings = o2t(GulpSettingsDO, {'subclassFrom': Computation, 'dbtablename':'gulpsettings'})
GulpSettings.job_builder = 'material_simulations/gulpSettings'
GulpSettings.actor = 'material_simulations/gulpSettings'
GulpSettings.result_retriever = 'material_simulations/gulpSettings'

