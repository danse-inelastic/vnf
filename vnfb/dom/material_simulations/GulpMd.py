

from _ import o2t

from vnf.dom.Computation import Computation

from mdt.orm.GulpMd import GulpMd
GulpMdTable = o2t(
    GulpMd, 
    {'subclassFrom': Computation, 
     'dbtablename':'gulpmd'},
    )
GulpMdTable.job_builder = 'material_simulations/gulp/md'
GulpMdTable.actor = 'material_simulations/gulp/md'
GulpMdTable.result_retriever = 'material_simulations/gulpSettings'

