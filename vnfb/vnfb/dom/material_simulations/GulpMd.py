

from _ import o2t

from vnfb.dom.Computation import Computation

from mdt.GulpMd import GulpMd
GulpMdTable = o2t(GulpMd, {'subclassFrom': Computation, 'dbtablename':'gulpsettings'})
GulpMdTable.job_builder = 'material_simulations/gulpSettings'
GulpMdTable.actor = 'material_simulations/gulpSettings'
GulpMdTable.result_retriever = 'material_simulations/gulpSettings'

