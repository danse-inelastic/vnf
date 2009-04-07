# -*- Python -*-
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#                                   Jiao Lin
#                      California Institute of Technology
#                        (C) 2008  All Rights Reserved
#
# {LicenseText}
#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#


from vnf.components.MaterialSimulationEngine import Engine

def materialSimulationEngines():
    return {
            'bvk': Engine('bvkcomputations', 'Born von Karman Lattice Dynamics', '', 'bvk'),
            'vacf': Engine('vacfcomputations','Velocity Autocorrelation Function','', 'vacf'),
#            'eisf': Engine('eisf','Elastic Incoherent Structure Factor','', 'eisf'),
#            'diffusionCoef': Engine('diffusionCoef','Diffusion Coefficient','', 'diffusionCoef'),
#            'sqeFromMd': Engine('sqeFromMd','S(Q,E) from Md','', 'sqeFromMd'),
#            'sqeFromPhonons': Engine('sqeFromPhonons','S(Q,E) from Phonons','', 'sqeFromPhonons'),
            }



# version
__id__ = "$Id$"

# End of file 
