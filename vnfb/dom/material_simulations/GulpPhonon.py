

from _ import o2t

from vnfb.dom.Computation import Computation

from mdt.GulpPhonon import GulpPhonon
GulpPhononTable = o2t(GulpPhonon, {'subclassFrom': Computation, 'dbtablename':'gulpphonon'})
GulpPhononTable.job_builder = 'material_simulations/gulpSettings'
GulpPhononTable.actor = 'material_simulations/gulpSettings'
GulpPhononTable.result_retriever = 'material_simulations/gulpSettings'

