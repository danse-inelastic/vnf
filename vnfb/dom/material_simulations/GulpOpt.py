

from _ import o2t

from vnfb.dom.Computation import Computation

from mdt.orm.GulpOpt import GulpOpt
GulpOptTable = o2t(
    GulpOpt, 
    {'subclassFrom': Computation, 
     'dbtablename':'gulpoptimizations'
     },
    )
GulpOptTable.job_builder = 'material_simulations/gulp/optimization'
GulpOptTable.actor = 'material_simulations/gulp/optimization'
GulpOptTable.result_retriever = 'material_simulations/gulp/optimization'

