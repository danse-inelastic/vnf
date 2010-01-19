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


typenames = [
    'neutron_experiment_simulations.neutron_components.SampleComponent.SampleComponent',
    'neutron_experiment_simulations.neutron_components.ChanneledGuide.ChanneledGuide',
    'neutron_experiment_simulations.neutron_components.DetectorSystem_fromXML.DetectorSystem_fromXML',
    'neutron_experiment_simulations.neutron_components.EMonitor.EMonitor',
    'neutron_experiment_simulations.neutron_components.FermiChopper.FermiChopper',
    'neutron_experiment_simulations.neutron_components.MonochromaticSource.MonochromaticSource',
    'neutron_experiment_simulations.neutron_components.NeutronPlayer.NeutronPlayer',
    'neutron_experiment_simulations.neutron_components.NeutronRecorder.NeutronRecorder',
    'neutron_experiment_simulations.neutron_components.PlaceHolder.PlaceHolder',
    'neutron_experiment_simulations.neutron_components.QEMonitor.QEMonitor',
    'neutron_experiment_simulations.neutron_components.QMonitor.QMonitor',
    'neutron_experiment_simulations.neutron_components.SNSModerator.SNSModerator',
    'neutron_experiment_simulations.neutron_components.SphericalPSD.SphericalPSD',
    'neutron_experiment_simulations.neutron_components.T0Chopper.T0Chopper',
    'neutron_experiment_simulations.neutron_components.TofMonitor.TofMonitor',
    'neutron_experiment_simulations.neutron_components.VanadiumPlate.VanadiumPlate',
    ]

def getTypes():
    from vnfb.dom import importType
    return map(importType, typenames)


# version
__id__ = "$Id$"

# End of file 
