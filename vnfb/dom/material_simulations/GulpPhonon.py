

from _ import o2t

from vnfb.dom.Computation import Computation

from mdt.orm.GulpPhonon import GulpPhonon
GulpPhononTable = o2t(
    GulpPhonon, 
    {'subclassFrom': Computation, 
     'dbtablename':'gulpphonon'},
    )
GulpPhononTable.job_builder = 'material_simulations/gulp/phonon'
GulpPhononTable.actor = 'material_simulations/gulp/phonon'
GulpPhononTable.result_retriever = 'material_simulations/gulp/phonon'

