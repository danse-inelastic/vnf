thispackage = 'vnf.dom.neutron_components'

def tables():
    tablenames = [
	'MonochromaticSource',
	'SNSModerator',
        'SNSModeratorMCSimulatedData',
	'ChanneledGuide',
	'T0Chopper',
	'FermiChopper',
	'SampleComponent',
	'QEMonitor',
	'QMonitor',
	'TofMonitor',
	'DetectorSystem_fromXML',
        'NeutronRecorder',
        ]
    
    tables = [
        getattr(_import('%s.%s' % (thispackage, name)),
                name)
        for name in tablenames
        ]
              
    return tables


def _import(package):
    return __import__(package, {}, {}, [''])
