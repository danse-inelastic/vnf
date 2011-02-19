

from _ import o2t

from vnfb.dom.Computation import Computation

from mdt.GulpOpt import GulpOpt
GulpOptTable = o2t(GulpOpt, {'subclassFrom': Computation, 'dbtablename':'gulpoptimizations'})
GulpOptTable.job_builder = 'material_simulations/gulpSettings'
GulpOptTable.actor = 'material_simulations/gulpSettings'
GulpOptTable.result_retriever = 'material_simulations/gulpSettings'

