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


# auto discovery
def findComponents(package='vnf.dom.neutron_experiment_simulations.neutron_components'):
    from vnf.dom.neutron_experiment_simulations.AbstractNeutronComponent import AbstractNeutronComponent
    pkg = __import__(package, {}, {}, [''])
    import os
    dir = os.path.dirname(pkg.__file__)
    entries = os.listdir(dir)
    comps = []
    for entry in entries:
        name, ext = os.path.splitext(entry)        
        if ext not in ['.py', '.pyc']: continue
        m = __import__('%s.%s' % (package, name), {}, {}, [''])
        cls = getattr(m, name, None)
        if not cls: continue
        try:
            issubkls = issubclass(cls, AbstractNeutronComponent)
        except:
            issubkls = False
        if not issubkls: continue
        if cls.abstract: continue
        if cls in comps: continue
        comps.append(cls)
        continue
    return comps



def _typename(kls):
    pre = '.'.join(kls.__module__.split('.')[2:])
    post = kls.__name__
    return '%s.%s' % (pre, post)
typenames = [_typename(kls) for kls in findComponents()]


'''
obsolete:

typenames = [
    'neutron_experiment_simulations.neutron_components.SampleComponent.SampleComponent',
    'neutron_experiment_simulations.neutron_components.ChanneledGuide.ChanneledGuide',
    'neutron_experiment_simulations.neutron_components.DetectorSystem_fromXML.DetectorSystem_fromXML',
    'neutron_experiment_simulations.neutron_components.EMonitor.EMonitor',
    'neutron_experiment_simulations.neutron_components.LMonitor.LMonitor',
    'neutron_experiment_simulations.neutron_components.FermiChopper.FermiChopper',
    'neutron_experiment_simulations.neutron_components.LMonitor.LMonitor',
    'neutron_experiment_simulations.neutron_components.MonochromaticSource.MonochromaticSource',
    'neutron_experiment_simulations.neutron_components.NeutronPlayer.NeutronPlayer',
    'neutron_experiment_simulations.neutron_components.NeutronRecorder.NeutronRecorder',
    'neutron_experiment_simulations.neutron_components.PlaceHolder.PlaceHolder'e,
    'neutron_experiment_simulations.neutron_components.QEMonitor.QEMonitor',
    'neutron_experiment_simulations.neutron_components.QMonitor.QMonitor',
    'neutron_experiment_simulations.neutron_components.SNSModerator.SNSModerator',
    'neutron_experiment_simulations.neutron_components.SphericalPSD.SphericalPSD',
    'neutron_experiment_simulations.neutron_components.T0Chopper.T0Chopper',
    'neutron_experiment_simulations.neutron_components.TofMonitor.TofMonitor',
    'neutron_experiment_simulations.neutron_components.VanadiumPlate.VanadiumPlate',
    ]
'''

getTypes = findComponents

# version
__id__ = "$Id$"

# End of file 
